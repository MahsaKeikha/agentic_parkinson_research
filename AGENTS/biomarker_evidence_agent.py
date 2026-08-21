class BiomarkerEvidenceAgent:
    name = "biomarker_evidence"

    def run(self, context):
        return {"agent": self.name, "task": "map biomarker evidence and uncertainty", "context": context}
