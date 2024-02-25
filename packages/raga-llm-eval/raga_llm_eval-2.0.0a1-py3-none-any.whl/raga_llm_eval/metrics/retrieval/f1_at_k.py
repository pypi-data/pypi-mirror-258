from .retrieval_metrics import RetrievalMetrics

class EvaluationMetricsAtK(RetrievalMetrics):
    def __init__(self, y_true, y_pred, k):
        """
        Initialize the evaluation metrics with true labels, predicted scores/labels, and the cut-off rank K.

        Parameters:
        - y_true: list or array of true binary labels (0 or 1) with the same length as y_pred.
        - y_pred: list or array of predicted scores or binary labels, sorted in descending order of relevance.
        - k: the number of top items to consider for calculating the metrics.
        """
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.k = k

    def precision_at_k(self):
        k = min(self.k, len(self.y_pred))
        num_relevant_items = sum(1 for i in self.y_pred[:k] if self.y_true[i] == 1)
        precision_at_k = num_relevant_items / k if k > 0 else 0
        return precision_at_k

    def recall_at_k(self):
        k = min(self.k, len(self.y_pred))
        total_relevant_items = sum(self.y_true)
        num_relevant_items_in_top_k = sum(1 for i in self.y_pred[:k] if self.y_true[i] == 1)
        recall_at_k = num_relevant_items_in_top_k / total_relevant_items if total_relevant_items > 0 else 0
        return recall_at_k

    def run(self):
        """Calculate F1 score at k using the precision and recall at k."""
        precision = self.precision_at_k()
        recall = self.recall_at_k()
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return f1_score
