def clinical_gate(context):
    blocked = any(k in context for k in ["diagnosis", "prescription", "treatment_authorization"])
    return {"allowed": not blocked, "requires_human_review": True}
