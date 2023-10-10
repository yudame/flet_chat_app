from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union
from icecream import ic
from langchain.chat_models import ChatOpenAI
import openai

from settings import AI_CONFIG
from stores.base_store import BaseStore
from stores.chat_store import Chat
from stores.user_store import User
from utils import strip_text_fragments, count_tokens, dict_to_cheat_sheet


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
        ]

    def _validate_config(self) -> None:
        self.ai_steps: Dict[str, Union[str, Dict]] = AI_CONFIG.get(
            "ai_steps",
            {
                "response": "predict the next message using 5 sentences or less",
            },
        )
        assert (
            "response" in self.ai_steps
        ), "openai_api_config.ai_steps is missing required key 'response'"

        openai_api_config = AI_CONFIG.get("openai_api", {})
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

    def prompt(
        self,
        chat: Chat,
        system_prompt: str,
        mode: str = "chat",
        max_tokens: Optional[int] = 90,  # 90 is about 3 long sentences
    ) -> str:
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
        total_tokens = count_tokens(full_message_text, self.openai_api_chat_model)
        if total_tokens > 2048:
            # todo: Handle token overflow
            return "Token limit exceeded"

        match mode:
            case "planning":
                ai_text_response = self.planning_llm.predict(
                    full_message_text, max_tokens=max_tokens
                )
            case "chat":
                ai_text_response = self.chat_llm.predict(
                    full_message_text, max_tokens=max_tokens
                )
            case _:
                raise ValueError(f"Invalid mode: {mode}")

        ai_text_response = ai_text_response.split(f"{self.ai_role.name}: ")[-1]
        ai_text_response = ai_text_response.split(f"{self.ai_role.title}: ")[-1]
        return ai_text_response

    def _generate_system_prompt(self, step_name: str, step_description: str) -> str:
        system_prompt = f'Now you, {self.ai_user.name}, take a moment to do a "{step_name}" step. {step_description}'
        if step_name in AI_CONFIG:
            cheat_sheet: str = dict_to_cheat_sheet(AI_CONFIG[step_name])
            system_prompt += f"Use this reference cheat sheet:\n\n{cheat_sheet}\n\n"
        if step_name not in ("practice", "response"):
            system_prompt += (
                "Be concise. Write a note to yourself using only a few words."
            )
        return system_prompt

    def _execute_planning_step(
        self, chat: Chat, step_name: str, step_description: str, max_tokens: int
    ) -> None:
        system_prompt = self._generate_system_prompt(step_name, step_description)

        ai_text_response = self.prompt(
            chat=chat,
            system_prompt=system_prompt,
            mode="planning",
            max_tokens=max_tokens,
        )

        ic(ai_text_response)
        chat.add_message(
            self.system_user, f"your notes on {step_name}:\n{ai_text_response}\n"
        )

    def _take_planning_steps(self, chat: Chat):
        for step_name, step_description in list(self.ai_steps.items())[:-1]:
            max_tokens = 120 if step_name == "practice" else 30

            self._execute_planning_step(chat, step_name, step_description, max_tokens)

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
