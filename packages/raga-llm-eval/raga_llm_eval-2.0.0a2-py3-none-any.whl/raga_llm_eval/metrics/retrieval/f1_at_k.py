from .retrieval_metrics import RetrievalMetrics

def to_relevance_scores_at_k(y_true, y_pred, K):
    """
    Adjusts the list of relevance scores for top K predictions.

    :param y_true: a list of relevant items
    :param y_pred: a list of predicted items, sorted by confidence or relevance
    :param K: the number of top items to consider
    :return: a list of binary relevance scores for the top K items
    """
    # Ensure y_pred is limited to top K items
    y_pred_k = y_pred[:K]
    rel_scores_k = [1 if d in y_true else 0 for d in y_pred_k]
    return rel_scores_k

class F1ScoreAtK(RetrievalMetrics):
    def __init__(self, y_true, y_pred, k):
        """
        Initialize F1ScoreAtK with true labels, predicted scores/labels, and the cut-off rank K.

        Parameters:
        - y_true: list or array of true binary labels (0 or 1) with the same length as y_pred.
        - y_pred: list or array of predicted scores or binary labels, sorted in descending order of relevance.
        - k: the number of top items to consider for calculating F1 score.
        """
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.k = k

    def run(self):
        k = min(self.k, len(self.y_pred))
        rel_score_k = to_relevance_scores_at_k(self.y_true, self.y_pred, k)
        precision = sum(rel_score_k) / k if k > 0 else 0
        total_relevant_items = sum(self.y_true)
        recall = sum(rel_score_k) / total_relevant_items if total_relevant_items > 0 else 0
        f1_score_at_k = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return f1_score_at_k

