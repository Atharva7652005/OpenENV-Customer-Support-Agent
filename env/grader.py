class Grader:
    def __init__(self, expected_logic):
        self.expected_logic = expected_logic

    def grade(self, history, final_status):
        taken_actions = []
        for msg in history:
            if msg.startswith("Agent ("):
                action_type = msg.split("(")[1].split(")")[0]
                taken_actions.append(action_type)
        
        correct_actions = [a for a in taken_actions if a in self.expected_logic]
        
        if len(correct_actions) == len(self.expected_logic):
            return 1.0
        elif len(correct_actions) > 0:
            return 0.5
        else:
            return 0.0
