def evaluate(result):
    required = ["workflow", "status"]
    return {"passed": all(key in result for key in required), "required": required}
