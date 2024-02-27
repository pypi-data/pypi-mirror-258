from ..metrics.retrieval import *

def context_retrieval_metrics_test(y_true, y_pred, metric_name, k=None, average='weighted', zero_division=1, threshold=0.5):
    """
    Test context retrieval metrics including precision, recall, F1 score, and their variations at K.

    Args:
        y_true (list): List of actual relevant item .
        y_pred (list): List of predicted items.
        metric_name (str): Name of the metric for evaluation ('Precision', 'Recall', 'F1Score', 'PrecisionAtK', 'RecallAtK', 'F1ScoreAtK').
        k (int): The number of top items to consider for 'AtK' metrics.
        average (str, optional): Averaging method for the computation. Defaults to 'weighted'.
        zero_division (int, optional): Sets the value to return when there is a zero division. Defaults to 1.
        threshold (float, optional): Threshold value for determining pass/fail status in evaluations. Defaults to 0.5.

    Returns:
        dict: A dictionary containing the evaluation results.
    """

    # Validate the metric name and ensure required parameters are provided for 'AtK' metrics
    valid_metrics = ['Precision', 'Recall', 'F1Score', 'PrecisionAtK', 'RecallAtK', 'F1ScoreAtK']
    if metric_name not in valid_metrics:
        raise ValueError(f"Invalid metric_name. Available metrics: {valid_metrics}")
    
    if 'AtK' in metric_name and k is None:
        raise ValueError("k parameter must be provided for 'AtK' metrics.")

    # Initialize and run the metric
    if 'AtK' in metric_name:
        metric_instance = globals()[metric_name](y_true, y_pred, k=k)
    else:
        metric_instance = globals()[metric_name](y_true, y_pred, average=average, zero_division=zero_division)
    
    score = metric_instance.run()


    # Determine if the calculated score passes the given threshold
    status = "Passed" if score >= threshold else "Failed"

    # Compile the results into a dictionary to return
    result = {
        "metric_name": metric_name,
        "score": score,
        "threshold": threshold,
        "is_passed": status
    }

    return result

