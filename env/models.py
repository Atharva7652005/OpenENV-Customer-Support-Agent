from pydantic import BaseModel, Field
from typing import List

class Observation(BaseModel):
    ticket: str = Field(description="The customer ticket text")
    priority: str = Field(description="Priority of the ticket (e.g., low, medium, high)")
    history: List[str] = Field(description="List of messages exchanged")
    status: str = Field(description="Current status of the ticket (e.g., open, in_progress, resolved)")

class Action(BaseModel):
    action_type: str = Field(description="Type of action: 'respond', 'refund', 'escalate', 'resolve'")
    message: str = Field(description="Message to the customer")

class Reward(BaseModel):
    score: float = Field(description="Reward score")
