class HumanReviewAgent:
    name = "human_review"

    def run(self, context):
        return {"agent": self.name, "requires_human_review": True, "context": context}
