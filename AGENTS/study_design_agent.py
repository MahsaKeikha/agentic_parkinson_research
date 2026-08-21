class StudyDesignAgent:
    name = "study_design"

    def run(self, context):
        return {"agent": self.name, "task": "draft research study design options", "context": context}
