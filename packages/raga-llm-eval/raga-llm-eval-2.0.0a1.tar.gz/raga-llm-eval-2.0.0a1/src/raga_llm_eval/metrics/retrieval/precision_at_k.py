
from .retrieval_metrics import RetrievalMetrics


class PrecisionAtK(RetrievalMetrics):
    def __init__(self, y_true, y_pred, k):
        """
        Initialize PrecisionAtK with true labels, predicted scores/labels, and the cut-off rank K.

        Parameters:
        - y_true: list or array of true binary labels (0 or 1) with the same length as y_pred.
        - y_pred: list or array of predicted scores or binary labels, sorted in descending order of relevance.
        - k: the number of top items to consider for calculating precision.
        """
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.k = k

    def run(self):
        k = min(self.k, len(self.y_pred))

        # Count the number of relevant items in the top-k predictions
        num_relevant_items = sum(1 for i in self.y_pred[:k] if self.y_true[i] == 1)

        # Calculate precision at k
        precision_at_k = num_relevant_items / k if k > 0 else 0
        return precision_at_k
