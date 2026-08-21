class EvidenceQualityAgent:
    name = "evidence_quality"

    def run(self, context):
        return {"agent": self.name, "task": "score evidence quality and missing data", "context": context}
