from env.models import Observation, Action, Reward
from env.state_manager import StateManager, is_repeating
from env.reward import RewardManager
from env.tasks import get_task
from env.grader import Grader

class CustomerSupportEnv:
    def __init__(self):
        self.state_manager = StateManager()
        self.reward_manager = None
        self.grader = None

    def reset(self, task_type: str) -> Observation:
        task_data = get_task(task_type)
        self.state_manager.reset_state(task_data)
        
        self.reward_manager = RewardManager(task_data["expected_logic"])
        self.grader = Grader(task_data["expected_logic"])
        
        state = self.state_manager.get_state()
        return Observation(
            ticket=state["ticket"],
            priority=state["priority"],
            history=state["history"],
            status=state["status"]
        )

    def step(self, action: Action):
        state_pre = self.state_manager.get_state()
        history_pre = state_pre["history"]
        pending_message = f"Agent ({action.action_type}): {action.message}"
        repeated_response = is_repeating(history_pre, pending_message)
        
        self.state_manager.update_state(action)
        state = self.state_manager.get_state()
        
        force_resolution = state["step_count"] > 2
        
        is_done = state["status"] in ["resolved", "escalated"] or state["step_count"] >= 4
        
        reward_score = self.reward_manager.calculate_step_reward(action, state["step_count"], is_done, repeated_response)
        
        # Add force_resolution penalty if step count goes too high without resolution
        if force_resolution and not is_done:
            reward_score -= 0.5
            reward_score = max(-1.0, reward_score)
        
        observation = Observation(
            ticket=state["ticket"],
            priority=state["priority"],
            history=state["history"],
            status=state["status"]
        )
        reward = Reward(score=reward_score)
        
        info = {}
        if is_done:
            info["grade"] = self.grader.grade(state["history"], state["status"])
            info["expected_logic"] = self.grader.expected_logic
            
        return observation, reward, is_done, info

    def state(self) -> Observation:
        state = self.state_manager.get_state()
        return Observation(
            ticket=state["ticket"],
            priority=state["priority"],
            history=state["history"],
            status=state["status"]
        )
