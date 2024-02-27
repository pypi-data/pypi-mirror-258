from sklearn.metrics import precision_score
from .retrieval_metrics import RetrievalMetrics

def to_relevance_scores(y_true, y_pred):
    """
    Returns a list of relevance scores (binary), which can be used in various metrics based on the intersection of y_true and y_pred.

    :param y_true: a list of relevant items (such as document ids)
    :param y_pred: a list of predicted items
    :return: a list of binary relevance scores, ex. [1, 0, 1, 1, 0, ...]
    """
    rel_scores = [1 if d in y_true else 0 for d in y_pred]
    return rel_scores

class Precision(RetrievalMetrics):
    def __init__(self, y_true, y_pred, average="weighted", zero_division=1):
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.average = average
        self.zero_division = zero_division

    def run(self):
        # This method directly returns the precision score computed by scikit-learn's f1_score function
        rel_scores = to_relevance_scores(self.y_true, self.y_pred)
        precision= precision_score(self.y_true, rel_scores, average=self.average, zero_division=self.zero_division)
        return precision
    


