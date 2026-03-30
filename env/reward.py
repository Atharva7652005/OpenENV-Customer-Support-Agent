from env.models import Action

class RewardManager:
    def __init__(self, expected_logic):
        self.expected_logic = expected_logic

    def calculate_step_reward(self, action: Action, step_count: int, is_done: bool):
        reward = 0.0
        
        if action.action_type in self.expected_logic:
            if action.action_type == "respond":
                reward += 0.3
            elif action.action_type in ["resolve", "refund", "escalate"]:
                reward += 0.5
        else:
            reward -= 0.3
            
        if is_done and step_count <= 2:
            reward += 0.2
            
        return reward
