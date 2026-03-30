def get_task(task_type: str):
    if task_type == "easy":
        return {
            "ticket": "My order hasn't arrived. It's been 2 days past the expected delivery date.",
            "priority": "low",
            "type": "delivery_issue",
            "expected_logic": ["respond", "resolve"]
        }
    elif task_type == "medium":
        return {
            "ticket": "I received a damaged product and I would like a refund or replacement ASAP.",
            "priority": "medium",
            "type": "product_issue",
            "expected_logic": ["refund"]
        }
    elif task_type == "hard":
        return {
            "ticket": "Your software is completely broken! It deleted all my data. I demand immediate escalation to a manager.",
            "priority": "high",
            "type": "technical_issue",
            "expected_logic": ["respond", "escalate"]
        }
    else:
        raise ValueError(f"Unknown task type: {task_type}")
