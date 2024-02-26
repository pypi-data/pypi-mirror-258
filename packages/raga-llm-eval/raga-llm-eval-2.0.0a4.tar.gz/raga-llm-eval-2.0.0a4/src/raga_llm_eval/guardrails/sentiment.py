
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

_lexicon = "vader_lexicon"

class Sentiment():
    """
    A sentiment scanner based on the NLTK's SentimentIntensityAnalyzer. It is used to detect if a prompt
    has a sentiment score lower than the threshold, indicating a negative sentiment.
    """

    def __init__(
            self,
            prompt: str,
            threshold: float = -0.1, 
            lexicon: str = _lexicon):
        """
        Initializes Sentiment with a threshold and a chosen lexicon.

        Parameters:
           threshold (float): Threshold for the sentiment score (from -1 to 1). Default is -0.1.
           lexicon (str): Lexicon for the SentimentIntensityAnalyzer. Default is 'vader_lexicon'.

        Raises:
           None.
        """

        nltk.download(lexicon)
        self._prompt = prompt
        self._sentiment_analyzer = SentimentIntensityAnalyzer()
        self._threshold = threshold

    def scan(self) -> (str, bool, float): # type: ignore
        result = {
            "prompt": self._prompt,
            "is_valid": True,
            "risk_score": 0.0,
        }
        prompt = self._prompt
        sentiment_score = self._sentiment_analyzer.polarity_scores(prompt)
        sentiment_score_compound = sentiment_score["compound"]
        if sentiment_score_compound > self._threshold:
            result["is_valid"] = True
            result["risk_score"] = 0.0
            result["sanitized_prompt"] = prompt

            return result
        
        # Normalize such that -1 maps to 1 and threshold maps to 0
        score = round((sentiment_score_compound - (-1)) / (self._threshold - (-1)), 2)


        result["is_valid"] = False
        result["risk_score"] = score
        result["sanitized_prompt"] = prompt
        return result