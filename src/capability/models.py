from typing import List, Optional

from pydantic import BaseModel, Field


class Action(BaseModel):
    action_type: str
    selector: Optional[str] = None
    value: Optional[str] = None


class Capability(BaseModel):
    name: str
    description: str
    actions: List[Action]
    parameters: List[str] = Field(default_factory=list)
    success_text: Optional[str] = None
    result_selector: Optional[str] = None