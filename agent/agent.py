import os
import json
from google import genai
from env.models import Observation, Action
from agent.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class SupportAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY environment variable is missing or invalid.")
        
        self.client = genai.Client(api_key=self.api_key)

    def select_action(self, observation: Observation) -> Action:
        history_str = "\n".join(observation.history) if observation.history else "None"
        
        user_prompt = USER_PROMPT_TEMPLATE.format(
            ticket=observation.ticket,
            priority=observation.priority,
            status=observation.status,
            history_str=history_str
        )
        
        # Combine system and user prompts and mandate JSON format
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}\n\nPlease output ONLY valid JSON without markdown wrapping."
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Upgraded generate_content call
                response = self.client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=full_prompt
                )
                
                content = response.text.strip() if response.text else ""
                
                # Safely strip markdown styling if it exists
                if content.startswith("```"):
                    lines = content.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    content = "\n".join(lines).strip()
                
                # Extract strict JSON envelope
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    content = content[start_idx:end_idx+1]
                    
                data = json.loads(content)
                
                # Fallback to defaults to prevent unhandled actions
                action_type = data.get("action_type", "respond")
                if action_type not in ["respond", "refund", "escalate", "resolve"]:
                    action_type = "respond"
                    
                return Action(
                    action_type=action_type,
                    message=data.get("message", "We are checking your issue.")
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Agent error fallback triggered: {e}")
                    return Action(action_type="respond", message="We are checking your issue.")
