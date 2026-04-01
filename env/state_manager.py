def is_repeating(history, message):
    return message in history[-2:]

class StateManager:
    def __init__(self):
        self.ticket = None
        self.priority = None
        self.history = []
        self.status = "open"
        self.step_count = 0

    def reset_state(self, ticket_data):
        self.ticket = ticket_data.get("ticket", "")
        self.priority = ticket_data.get("priority", "low")
        self.history = []
        self.status = "open"
        self.step_count = 0

    def update_state(self, action):
        self.step_count += 1
        self.history.append(f"Agent ({action.action_type}): {action.message}")
        
        # State progression logic based on action_type
        if action.action_type in ["refund", "escalate"]:
            self.status = "resolved" if action.action_type == "refund" else "escalated"
        elif action.action_type == "resolve":
            self.status = "resolved"
        elif action.action_type == "respond":
            self.status = "in_progress"

    def get_state(self):
        return {
            "ticket": self.ticket,
            "priority": self.priority,
            "history": self.history.copy(),
            "status": self.status,
            "step_count": self.step_count
        }
