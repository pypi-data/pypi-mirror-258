from sklearn.metrics import f1_score
from .retrieval_metrics import RetrievalMetrics
def filter_kwargs(kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

class F1Score(RetrievalMetrics):
    def __init__(self, y_true, y_pred, **kwargs):
        super().__init__()
        self.y_true = y_true
        self.y_pred = y_pred
        self.average = kwargs.get("average", "binary")

    def run(self):
        # This method directly returns the F1 score computed by scikit-learn's f1_score function
        filtered_kwargs = filter_kwargs({"average": self.average})
        f1_score = f1_score(self.y_true, self.y_pred, **filtered_kwargs)
        return f1_score
    
    
