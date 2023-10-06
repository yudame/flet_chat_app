from dataclasses import dataclass
from datetime import datetime
import json
import logging
import os
from typing import Dict, List

from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage, BaseMessage

from stores.base_store import BaseStore
from stores.chat_store import Chat
from stores.user_store import User


@dataclass(frozen=True, slots=True)
class Prompt:
    summary: str
    key_points: List[str]
    new_message: str
    timestamp: datetime = datetime.utcnow()


@dataclass(frozen=True, slots=True)
class AIRole:
    name: str
    title: str
    intro: str


class AIStore(BaseStore):
    # __slots__ = ["id", "openai_api_key", "openai_api_org", "openai_api_model", "llm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.page is provided by the BaseStore class

        ai_config: Dict = json.loads(os.environ.get("AI_CONFIG"))
        openai_api_config = ai_config.get("openai_api", {})

        self.openai_api_key: str = openai_api_config.get("api_key")
        self.openai_api_org: str = openai_api_config.get("org_id")
        self.openai_api_model: str = openai_api_config.get("model")

        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            openai_organization=self.openai_api_org,
            model_name=self.openai_api_model,
            temperature=0,
        )

        # Define the behavior instruction for the chat model
        self.ai_role = AIRole(**ai_config.get("ai_role", {}))
        self.ai_user = User(id=self.ai_role.name, name=self.ai_role.name)
        behavior_instruction = self.ai_role.intro + (
            "\n\n" "Current conversation:\n" "{history}\n" "Human: {input}\n"
        )

        # Create a PromptTemplate instance with history and input variables
        prompt_template = PromptTemplate(
            input_variables=["history", "input"], template=behavior_instruction
        )

        # Initialize the conversation chain with the formatted prompt template
        memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm, prompt=prompt_template, memory=memory
        )

    def prompt(self, chat: Chat, prompt_text: str, user: User) -> str:
        # Convert past messages to a string format for the history variable
        history = "\n".join(
            f"{message.author.name}: {message.message}"
            for message in chat.get_message_history()
        )

        ai_text_response: str = self.conversation.predict(
            input=prompt_text, history=history
        )

        print(ai_text_response)
        return ai_text_response
