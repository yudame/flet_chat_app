import json
from json import JSONDecodeError
from typing import Dict

AI_CONFIG: Dict = {}

try:
    with open("settings/ai_config.json", "r") as f:
        AI_CONFIG = json.loads(f.read())
except FileNotFoundError:
    print(
        "Failed to load AI_CONFIG from assets/ai_config.json "
        "Make a copy of assets/ai_config_template.json and fill in the values.  "
        "See README for more info."
    )
except JSONDecodeError:
    print(
        "Failed to parse AI_CONFIG from assets/ai_config.json "
        "Make sure the file is valid JSON."
    )

APP_CONFIG: Dict = {
    "name": "Not A Therapist App by Official",
    "title": "AI Chat Demo",
    "assets_dir": "assets",
    "upload_dir": "assets/uploads",
}
