from env.models import Observation, Action, Reward
from env.state_manager import StateManager
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
        self.state_manager.update_state(action)
        state = self.state_manager.get_state()
        
        is_done = state["status"] in ["resolved", "escalated"] or state["step_count"] >= 5
        
        reward_score = self.reward_manager.calculate_step_reward(action, state["step_count"], is_done)
        
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
