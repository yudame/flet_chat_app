from dataclasses import dataclass
import json
import logging
import os
from typing import List, Set, Dict, Optional, Tuple, AbstractSet
from datetime import datetime
import uuid
import flet as ft
from langchain import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

from stores.base_store import BaseStore


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

        from langchain.chat_models import ChatOpenAI

        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            openai_organization=self.openai_api_org,
            model_name=self.openai_api_model,
            temperature=0.5,
        )

        ai_role = AIRole(**ai_config.get("ai_role", {}))

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", ai_role.intro),
                ("human", "{text}"),
            ]
        )

        self.conversation_chain = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(
                # ai_prefix=bot_name, human_prefix=human_name
            ),
        )
        self.conversation_chain.prompt = PromptTemplate(
            input_variables=["messages", "input"],
            template=CONVERSATION_TEMPLATE.format(
                # human_name=self.human_name,
                # bot_name=self.bot_name,
                input="{input}",
                history="{messages}",
            ),
        )
        self.conversation_chain.prep_prompts(
            [
                {
                    "input": "{input}",
                    f"messages": (prev_history + "\n" if prev_history else "")
                    + "{messages}",
                },
            ]
        )

    @property
    def history_as_text(self) -> str:
        return "\n".join(
            [
                ("Human: " if m.type == "human" else "AI: ") + m.content
                for m in self.conversation_chain.memory.chat_memory.messages
            ]
        )

    def prompt(self, prompt_text: str):
        with get_openai_callback() as cb:
            result: str = self.conversation_chain.run(
                {
                    "messages": self.history_as_text,
                    "input": prompt_text,
                }
            )
            logging.info(f"Spent a total of {cb.total_tokens} tokens")
        return result

    def to_dict(self):
        return {
            "keep_context": self.keep_context,
            "summarize_context": self.summarize_context,
            "bot_name": self.bot_name,
            "human_name": self.human_name,
            "prev_history": self.history_as_text,
        }

    def get_new_ai_message(self):
        pass

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


CONVERSATION_TEMPLATE = """
The following is a productive and efficient conversation between {human_name} and {bot_name}. 
{human_name} leads the conversation and informs {bot_name} on what is important to talk about.
{bot_name} is kind and provides lots of specific details on subjects it knows about. 
If {bot_name} does not know the answer to a question, it honestly admits that it does not know. 
It may provide a good guess and note that it's just a guess.

Current conversation:
{messages}
{human_name}: {input}
{bot_name}:
"""
