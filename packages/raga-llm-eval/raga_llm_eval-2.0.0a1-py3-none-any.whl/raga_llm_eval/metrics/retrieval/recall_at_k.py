from .retrieval_metrics import RetrievalMetrics

class RecallAtK(RetrievalMetrics):
    def __init__(self, y_true, y_pred, k):
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.k = k

    def run(self):
        k = min(self.k, len(self.y_pred))
        total_relevant_items = sum(self.y_true)

        # Count the number of relevant items in the top-k predictions
        num_relevant_items_in_top_k = sum(1 for i in self.y_pred[:k] if self.y_true[i] == 1)

        # Calculate recall at k
        recall_at_k = num_relevant_items_in_top_k / total_relevant_items if total_relevant_items > 0 else 0
        return recall_at_k
