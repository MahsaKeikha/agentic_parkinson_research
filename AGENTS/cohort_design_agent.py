class CohortDesignAgent:
    name = "cohort_design"

    def run(self, context):
        return {"agent": self.name, "task": "define research cohort criteria", "context": context}
