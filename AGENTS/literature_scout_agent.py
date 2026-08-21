class LiteratureScoutAgent:
    name = "literature_scout"

    def run(self, context):
        return {"agent": self.name, "task": "identify relevant Parkinson research evidence", "context": context}
