from ..base_metrics import Metrics


class RetrievalMetrics(Metrics):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
