from settings.ai_datatypes import AIConfig, LLMStepName, LLMStep, AIRole


AI_CONFIG = AIConfig(
    openai_api={
        "api_key": "",
        "org_id": "",
        "default_model": "gpt-3.5-turbo",
        "planning_model": "text-davinci-003",
        "chat_model": "gpt-4",
    },
    ai_role=AIRole(
        name="AI Bot",
        title="general assistant",
        intro="The following is a productive and efficient conversation between a human and an AI bot.\n"
        "The human leads the conversation and informs the bot on what is important to talk about.\n"
        "The bot is kind and provides lots of specific details on subjects it knows about.\n"
        "If the bot does not know the answer to a question, it honestly admits that it does not know.\n"
        "It may provide a good guess and note that it's just a guess.",
        first_message="Hello, I'm here to help if I can. What's on your mind?",
    ),
    llm_steps=[
        LLMStep(
            name="step_N_concept",
            instruction="Instructions for Step 1..N, given to AI role",
            cheat_sheet={
                "category_1": {"topic 1": "description", "topic 2": "description"},
                "category_2": {"topic 1": "description", "topic 2": "description"},
            },
        ),
        LLMStep(
            name=LLMStepName.PRACTICE,
            instruction="Given where the conversation has gone so far, jot down some ideas on what do say next.",
            cheat_sheet=None,
        ),
        LLMStep(
            name=LLMStepName.RESPONSE,
            instruction="Final instruction to generate the response.  This will be the only output seen by users.",
            cheat_sheet=None,
        ),
    ],
)
