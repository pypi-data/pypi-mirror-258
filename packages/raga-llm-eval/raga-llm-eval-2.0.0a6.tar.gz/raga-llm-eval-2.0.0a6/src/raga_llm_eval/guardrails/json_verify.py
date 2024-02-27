import json
import re

import json_repair
import regex

JSON_PATTERN = r"(?<!\\)(?:\\\\)*\{(?:[^{}]|(?R))*\}"


class JSONVerify:
    def __init__(
        self, question, response, required_elements=0, repair = True
    ):
        """
        Initialize the TokenLimit object.

        Args:
        question (str): The question to be asked.
        response (str): The response to be evaluated.
        required_elements (int, optional): The minimum number of JSON elements
        that should be present. Defaults to 0.
        repair (bool, optional): Whether to repair the broken JSON. Defaults to False.
        """
        self.question = question
        self.output = response
        self._repair = repair
        self._required_elements = required_elements
        self._pattern = regex.compile(JSON_PATTERN, re.DOTALL)

    def is_valid_json(self, json_str: str) -> bool:
        """Check if the input string is a valid JSON.

        Parameters:
            json_str (str): The input string to check.

        Returns:
            bool: True if the input string is a valid JSON, False otherwise.
        """
        try:
            json.loads(json_str)
            return True
        except:
            return False

    def repair_json(self, json_str: str) -> str:
        """Repair a broken JSON string.

        Parameters:
            json_str (str): The input string to repair.

        Returns:
            str: The repaired JSON string.
        """

        try:
            repaired_json = json_repair.repair_json(
                json_str, skip_json_loads=True, return_objects=False
            )
        except:
            return json_str

        return repaired_json

    def run(self):
        score = 0.0
        if self.question.strip() == "":
            score = 1.0

        # Find JSON object and array candidates using regular expressions
        json_candidates = self._pattern.findall(self.output)

        # Validate each JSON
        valid_jsons = []
        for json_candidate in json_candidates:
            if self.is_valid_json(json_candidate):
                valid_jsons.append(json_candidate)
                continue

            if self._repair:
                repaired_json = self.repair_json(json_candidate)
                valid_jsons.append(repaired_json)
                self.output = self.output.replace(json_candidate, repaired_json)

            # Check if there are enough valid JSONs
            if len(valid_jsons) < self._required_elements:
                score = 0.0

            # Compare
            if len(valid_jsons) != len(json_candidates):
                score = 0.0

            score = 1.0

        result = {
            "input": self.question,
            "response": self.output,
            "is_passed": "Passed" if score else "Failed",
            "repaired_json": self.output,
            "score": score,
        }

        return result
