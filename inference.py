import os
from dotenv import load_dotenv
from env.environment import CustomerSupportEnv
from agent.agent import SupportAgent

def run_evaluation():
    load_dotenv()
    
    env = CustomerSupportEnv()
    try:
        agent = SupportAgent()
    except ValueError as e:
        print(f"Error initializing agent: {e}")
        print("Please set your GEMINI_API_KEY in a .env file or environment variable.")
        return

    tasks = ["easy", "medium", "hard"]
    
    print("Starting OpenEnv Evaluation: Customer Support\n" + "="*50)
    
    for task_type in tasks:
        print(f"\n--- Running Task: {task_type.capitalize()} ---")
        
        observation = env.reset(task_type)
        done = False
        step = 0
        total_step_reward = 0.0
        
        while not done:
            step += 1
            print(f"\n[Step {step}]")
            print(f"Observation | Status: {observation.status}")
            
            action = agent.select_action(observation)
            print(f"Agent Action | Type: {action.action_type} | Message: {action.message}")
            
            observation, reward, done, info = env.step(action)
            total_step_reward += reward.score
            
            print(f"Step Reward: {reward.score:.2f}")

        final_grade = info.get("grade", 0.0)
        print(f"\nTask: {task_type.capitalize()}")
        print(f"Reward: {final_grade:.1f}")

if __name__ == "__main__":
    run_evaluation()
