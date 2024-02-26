from enum import Enum
from typing import Dict, List, Optional, Sequence, Union
# from utils import calculate_risk_score
from anonymize_helpers.transformers_helpers import pipeline
import nltk


def calculate_risk_score(score: float, threshold: float) -> float:
    if score > threshold:
        return 1.0

    risk_score = round(abs(score - threshold) / threshold, 1)
    # Ensure risk score is between 0 and 1
    return min(max(risk_score, 0), 1)

def split_text_by_sentences(text: str) -> List[str]:
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    return nltk.sent_tokenize(text.strip())

model_path = (
    "papluca/xlm-roberta-base-language-detection",
    "ProtectAI/xlm-roberta-base-language-detection-onnx",
)


class MatchType(Enum):
    SENTENCE = "sentence"
    FULL = "full"

    def get_inputs(self, prompt: str) -> List[str]:
        if self == MatchType.SENTENCE:
            return split_text_by_sentences(prompt)

        return [prompt]


class Language():
    """
    A class for scanning the prompt for language detection.

    Note: when no languages are detected above the threshold, the prompt is considered valid.
    """

    def __init__(
        self,
        prompt: str,
        valid_languages: Sequence[str]= ["en"],
        threshold: float = 0.6,
        match_type: Union[MatchType, str] = MatchType.FULL,
        use_onnx: bool = False,
        transformers_kwargs: Optional[Dict] = None,
    ):
        """
        Initializes the Language scanner with a list of valid languages.

        Parameters:
            prompt (str): The prompt to check for language.
            valid_languages (Sequence[str]): A list of valid language codes in ISO 639-1, default is ["en"].
            threshold (float): Minimum confidence score.
            match_type (MatchType): Whether to match the full text or individual sentences. Default is MatchType.FULL.
            use_onnx (bool): Whether to use ONNX for inference. Default is False.
            transformers_kwargs (Optional[Dict]): Optional keyword arguments for the transformers pipeline.
        """
        if isinstance(match_type, str):
            match_type = MatchType(match_type)

        self._prompt = prompt
        self._threshold = threshold
        self._valid_languages = valid_languages
        self._match_type = match_type

        transformers_kwargs = transformers_kwargs or {}
        transformers_kwargs["max_length"] = 512
        transformers_kwargs["truncation"] = True
        transformers_kwargs["top_k"] = None

        self._pipeline = pipeline(
            task="text-classification",
            model=model_path[0],
            onnx_model=model_path[1],
            use_onnx=use_onnx,
            **transformers_kwargs,
        )

    def run(self) -> Dict[str, Union[str, bool, float]]:
        result = {'prompt': self._prompt, 'is_valid': True, 'risk_score': 0.0}

        if self._prompt.strip() == "":
            return result
        
        prompt = self._prompt

        results_all = self._pipeline(self._match_type.get_inputs(prompt))
        for result_chunk in results_all:
            languages_above_threshold = [
                result["label"] for result in result_chunk if result["score"] > self._threshold
            ]

            highest_score = max([result["score"] for result in result_chunk])

            # Check if any of the languages above threshold are not valid
            if len(set(languages_above_threshold) - set(self._valid_languages)) > 0:
                result['is_valid'] = False
                result['sanitized_prompt'] = prompt
                result['risk_score'] = calculate_risk_score(highest_score, self._threshold)
                return result

        return result