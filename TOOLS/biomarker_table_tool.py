def build_biomarker_table(items):
    return [{"biomarker": item, "evidence_status": "review_required"} for item in items]
