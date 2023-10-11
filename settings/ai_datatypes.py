from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Union


@dataclass(frozen=True, slots=True)
class AIRole:
    name: str
    title: str
    intro: str
    first_message: str


RecursiveDict = Dict[str, Union[str, "RecursiveDict"]]


class LLMStepName(Enum):
    PRACTICE = "practice"
    RESPONSE = "response"


@dataclass(frozen=True, slots=True)
class LLMStep:
    name: Union[str, LLMStepName]
    instruction: str
    cheat_sheet: Optional[Union[str, RecursiveDict]]


class AIConfig:
    __slots__ = ["openai_api", "ai_role", "llm_steps"]

    def __init__(
        self,
        openai_api: Dict[str, str],
        ai_role: AIRole,
        llm_steps: List[LLMStep],
    ) -> object:
        self.openai_api = openai_api
        self.ai_role = ai_role
        self.llm_steps = llm_steps
