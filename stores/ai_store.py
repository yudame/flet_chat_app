from dataclasses import dataclass
from datetime import datetime
from typing import List

from langchain.chat_models import ChatOpenAI

from settings import AI_CONFIG
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
    first_message: str


class AIStore(BaseStore):
    # __slots__ = ["id", "openai_api_key", "openai_api_org", "openai_api_model", "llm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.page is provided by the BaseStore class
        self._validate_config()
        self.planning_llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            openai_organization=self.openai_api_org,
            model_name=self.open_ai_planning_model,
            temperature=0.1,
        )
        self.chat_llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            openai_organization=self.openai_api_org,
            model_name=self.openai_api_chat_model,
            temperature=0.7,
        )

        self.ai_user = User(id=self.ai_role.name, name=self.ai_role.name)
        self.system_user = User(id="system", name="system")
        self.conversation_start_message_list = [
            {"role": "system", "content": self.ai_role.intro},
            # {"role": "user", "content": "Hello, I'd like to talk."},
            {
                "role": self.ai_role.title,
                "content": self.ai_first_message,
            },
        ]

    def _validate_config(self):
        openai_api_config = AI_CONFIG.get("openai_api", {})
        ai_steps = AI_CONFIG.get(
            "ai_steps",
            {"response": "predict the next message using 5 sentences or less"},
        )
        assert (
            "response" in ai_steps
        ), "openai_api_config.ai_steps is missing required key 'response'"

        self.openai_api_key: str = openai_api_config.get("api_key")
        self.openai_api_org: str = openai_api_config.get("org_id")
        default_model: str = openai_api_config.get("default_model")
        self.openai_api_chat_model: str = (
            openai_api_config.get("chat_model") or default_model
        )
        self.open_ai_planning_model: str = (
            openai_api_config.get("planning_model") or default_model
        )

        # Define the behavior instruction for the chat model
        self.ai_role = AIRole(**AI_CONFIG.get("ai_role", {}))
        self.ai_steps: dict = AI_CONFIG.get("ai_steps", {})
        self.ai_first_message = AI_CONFIG.get(
            "ai_first_message", "Hi, where should we start?"
        )

    def prompt(self, chat: Chat, system_prompt: str, mode: str = "chat") -> str:
        messages_list: List = []
        # load summary if exists
        if chat.summary:
            messages_list.append(
                {
                    "role": "system",
                    "content": f"Here is a summary of conversation until now: {chat.summary}",
                }
            )
        else:
            messages_list += self.conversation_start_message_list
        # add all message history until now
        messages_list += chat.get_history_as_message_list()
        # add next step
        messages_list.append({"role": "system", "content": system_prompt})

        # convert to text
        full_message_text: str = "\n".join(
            [f"{message['role']}: {message['content']}" for message in messages_list]
        )

        match mode:
            case "planning":
                ai_text_response = self.planning_llm.predict(full_message_text)
            case "chat":
                ai_text_response = self.chat_llm.predict(full_message_text)
            case _:
                raise ValueError(f"Invalid mode: {mode}")

        print(ai_text_response)
        return ai_text_response

    def _take_planning_steps(self, chat: Chat):
        step_response_additions = []
        for step_name, step_description in list(self.ai_steps.items())[
            :-1
        ]:  # Skip the last step
            ai_text_response = self.prompt(
                chat=chat, system_prompt=step_description, mode="planning"
            )
            step_response_additions.append(ai_text_response)
            chat.add_message(self.ai_user, ai_text_response)
            # stop forcing the prompt method to keep recompiling the history

    def get_next_message(self, chat: Chat):
        self._take_planning_steps(chat=chat)

        final_system_prompt = self.ai_steps.get(
            "response", "take a deep breath and prepare your best response"
        )
        ai_text_response = self.prompt(
            chat=chat, system_prompt=final_system_prompt, mode="chat"
        )

        chat.add_message(self.ai_user, ai_text_response)
        return ai_text_response
