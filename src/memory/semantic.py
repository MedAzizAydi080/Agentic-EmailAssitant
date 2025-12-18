import json
import os
from ..config import DATA_DIR

class SemanticMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_path = os.path.join(DATA_DIR, "memory", f"{user_id}_profile.json")
        self.profile = self._load_profile()

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as f:
                return json.load(f)
        return {"name": "User", "preferences": {}}

    def update_profile(self, key: str, value: any):
        self.profile[key] = value
        self._save_profile()

    def _save_profile(self):
        with open(self.profile_path, "w") as f:
            json.dump(self.profile, f, indent=2)

    def get_context_str(self):
        return f"User Profile: {json.dumps(self.profile)}"
