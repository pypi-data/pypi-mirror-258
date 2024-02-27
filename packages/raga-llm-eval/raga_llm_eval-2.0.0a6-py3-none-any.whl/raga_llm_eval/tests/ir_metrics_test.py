from ..metrics.retrieval import *

def ir_metrics_test(query_relevance, runs, metric_name, rel, cutoff, min_rel, max_rel, p, normalize, T, recall, alpha, judged_only, dcg, gains, beta, relative, threshold):
    
    
    """
    Initializes the class instance with the provided parameters.

    Args:
        query_relevance: Mapping of queries to documents with relevance scores for evaluation.
        runs: Results of retrieval runs, including query IDs and ranked documents.
        metric_name: Name of the metric for evaluation (e.g., 'nDCG', 'Precision').
        rel: Relevance threshold to distinguish relevant from non-relevant documents.
        cutoff: Ranking position at which evaluation is truncated.
        min_rel: Minimum relevance score that can be assigned to a document.
        max_rel: Maximum relevance score that can be assigned to a document.
        p: Persistence parameter used in metrics like Rank-Biased Precision.
        normalize: Boolean indicating if the metric score should be normalized.
        T: Total desired gain or threshold for some metrics.
        recall: Recall level for precision at recall calculations.
        alpha: Redundancy intolerance parameter in diversity metrics.
        judged_only: Boolean to consider only documents that have been judged.
        dcg: Specifies the DCG formulation to use in nDCG calculations.
        gains: Custom gain mapping for non-standard relevance-to-gain mappings.
        beta: Specifies relative importance of recall to precision in F-score.
        relative: Boolean for calculating precision relative to maximum possible SetP.
        threshold: Threshold value for determining pass/fail status in evaluations.
        
    Returns:
        dict: A dictionary containing the evaluation results.

    """

    
    # List of all supported measures. This list should be updated as new measures are implemented.
    all_measures = [
        "Accuracy",
        "AP",
        "BPM",
        "Bpref",
        "Compat",
        "infAP",
        "INSQ",
        "INST",
        "IPrec",
        "Judged",
        "nDCG",
        "NERR10",
        "NERR11",
        "NERR8",
        "NERR9",
        "NumQ",
        "NumRel",
        "NumRet",
        "P",
        "R",
        "Rprec",
        "SDCG",
        "SetAP",
        "SetF",
        "SetP",
        "SetR",
        "Success"
    ]
    
    # Check if the specified metric name is among the supported measures.
    if metric_name not in all_measures:
        raise ValueError("Invalid metric_name. Available metric_name: ", all_measures)
    
    # Dynamically create an instance of the specified metric with provided parameters.
    measure_instance = globals()[metric_name](
        qrels=query_relevance,
        runs=runs,
        rel=rel,
        cutoff=cutoff,
        min_rel=min_rel,
        max_rel=max_rel,
        p=p,
        normalize=normalize,
        T=T,
        recall=recall,
        alpha=alpha,
        judged_only=judged_only,
        dcg=dcg,
        gains=gains,
        beta=beta,
        relative=relative,
    )
    
    # Calculate the score using the instantiated metric.
    score = measure_instance.run()
    
    # Determine if the calculated score passes the given threshold.
    status = "Passed" if score > threshold else "Failed"

    # Compile the results into a dictionary to return.
    result = {
        "prompt": query_relevance, 
        "context": runs,  
        "score": score,  
        "is_passed": status,
    }
    
    return result
