from typing import Dict, Optional, Sequence
from presidio_anonymizer.core.text_replace_builder import TextReplaceBuilder
from span_marker import SpanMarkerModel


MODEL_BASE = {
    "path": "tomaarsen/span-marker-bert-base-orgs",
}

MODEL_SMALL = {
    "path": "tomaarsen/span-marker-bert-small-orgs",
}

ALL_MODELS = [MODEL_BASE, MODEL_SMALL]

class BanCompetitors:
    """
    Scanner to detect competitors in a prompt.

    It uses a named-entity recognition model to extract organizations from the prompt and compares them to a list of competitors.
    """

    def __init__(
        self,
        prompt: str,
        competitors: Sequence[str],
        threshold: float = 0.5,
        redact: bool = True,
        model: Optional[Dict] = None,
    ):
        """
        Initialize BanCompetitors object.

        Parameters:
            prompt (str): Prompt to check for competitors.
            competitors (Sequence[str]): List of competitors to detect.
            threshold (float, optional): Threshold to determine if a competitor is present in the prompt. Default is 0.5.
            redact (bool, optional): Whether to redact the competitor name. Default is True.
            model (Dict, optional): Model to use for named-entity recognition. Default is BASE model.

        Raises:
            ValueError: If no topics are provided.
        """
        if model is None:
            model = MODEL_BASE

        if model not in ALL_MODELS:
            raise ValueError(f"Model must be in the list of allowed: {ALL_MODELS}")

        self._prompt = prompt
        self._competitors = competitors
        self._threshold = threshold
        self._redact = redact
        self._model_name = model["path"]
        self._ner_pipeline = SpanMarkerModel.from_pretrained(
            model["path"], labels=["ORG"]
        )

        # if device().type == "cuda":
        #     self._ner_pipeline = self._ner_pipeline.cuda()

    def run(self: str) -> (str, bool, float): # type: ignore
        is_detected = False
        text_replace_builder = TextReplaceBuilder(original_text=self._prompt)
        entities = self._ner_pipeline.predict(self._prompt)
        # print(entities)
        # print(self._competitors)
        entities = sorted(entities, key=lambda x: x["char_end_index"], reverse=True)
        for entity in entities:
            if entity["span"] not in self._competitors:
                continue

            if entity["score"] < self._threshold:
                reason = (
                    "Competitor detected but the score is below threshold",
                    "entity:", entity["span"],
                    "score:", entity["score"],
                )
                continue

            is_detected = True

            if self._redact:
                text_replace_builder.replace_text_get_insertion_index(
                    "[REDACTED]",
                    entity["char_start_index"],
                    entity["char_end_index"],
                )
            reason = (
                "Competitor detected with score", 
                "entity:", entity["span"],
                "score:", entity["score"],
            )

        if is_detected:
            sanitized_prompt = text_replace_builder.output_text
            is_valid = False
            risk_score = 1.0
        else:
            sanitized_prompt = self._prompt
            is_valid = True
            risk_score = 0.0

        result = {
            "input": self._prompt,
            "sanitized_prompt": sanitized_prompt,
            "is_valid": is_valid,
            "risk_score": risk_score,
            "reason": reason,
            "threshold": self._threshold,
            "evaluated_with": {"model": self._model_name},
        }

        return result

