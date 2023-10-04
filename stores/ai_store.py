from dataclasses import dataclass
import json
import os
from typing import List, Set, Dict, Optional, Tuple, AbstractSet
from datetime import datetime
import uuid
from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


@dataclass(frozen=True, slots=True)
class Prompt:
    summary: str
    key_points: List[str]
    new_message: str
    timestamp: datetime = datetime.utcnow()


class AI:
    # __slots__ = ["id", "openai_api_key", "openai_api_org", "openai_api_model", "llm"]

    def __init__(self):
        self.id: str = str(uuid.uuid4())

        openai_api_config = json.loads(os.environ.get("AI_CONFIG")).get(
            "openai_api", {}
        )

        self.openai_api_key: str = openai_api_config.get("api_key")
        self.openai_api_org: str = openai_api_config.get("org_id")
        self.openai_api_model: str = openai_api_config.get("model")

        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=self.openai_api_key,
            openai_organization=self.openai_api_org,
            model_name=self.openai_api_model,
        )
