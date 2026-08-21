AGENT_ORDER = ["literature_scout", "cohort_design", "biomarker_evidence", "study_design", "evidence_quality", "human_review"]

def orchestrate(context):
    return {"workflow": AGENT_ORDER, "context": context, "status": "review_required"}
