from env.models import Action

class RewardManager:
    def __init__(self, expected_logic):
        self.expected_logic = expected_logic

    def calculate_step_reward(self, action: Action, step_count: int, is_done: bool, repeated_response: bool = False):
        reward = 0.0
        
        # Good response
        if action.action_type == "respond":
            reward += 0.2
            
        # Resolution actions
        if action.action_type in ["refund", "escalate", "resolve"]:
            reward += 0.6
            
        # Fast resolution bonus
        if is_done and step_count <= 2:
            reward += 0.2
            
        # Penalize repeated responses
        if repeated_response:
            reward -= 0.3
            
        # Penalize no progress
        if step_count > 3:
            reward -= 0.2
            
        # Clamp reward
        return max(-1.0, min(1.0, reward))
