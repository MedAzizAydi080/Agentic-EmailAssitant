import os
from ..config import PROMPTS_DIR

class ProceduralMemory:
    def __init__(self):
        self._ensure_defaults()

    def _ensure_defaults(self):
        defaults = {
            "triage.txt": """You are an expert support triage agent.
Your job is to decide if a user query can be answered immediately with your knowledge + similar past examples, OR if it requires deep research (RAG).

Respond with a JSON object: {"decision": "respond" | "research" | "ignore", "reasoning": "..."}

Examples of past decisions:
{examples}

User Query: {query}
""",
            "response.txt": """You are a helpful support agent.
Answer the user query based on the context provided.
Context: {context}

User Query: {query}
"""
        }
        
        for name, content in defaults.items():
            path = os.path.join(PROMPTS_DIR, name)
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)

    def load_prompt(self, name: str) -> str:
        # name like 'triage' (without .txt)
        path = os.path.join(PROMPTS_DIR, f"{name}.txt")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return ""

    def update_prompt(self, name: str, new_content: str):
        path = os.path.join(PROMPTS_DIR, f"{name}.txt")
        with open(path, "w") as f:
            f.write(new_content)
