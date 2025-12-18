import sqlite3
import json
from ..config import MEMORY_DB_PATH

class EpisodicMemory:
    def __init__(self):
        self.conn = sqlite3.connect(MEMORY_DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                output_text TEXT,
                label TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_episode(self, input_text: str, output_text: str, label: str):
        self.cursor.execute(
            "INSERT INTO episodes (input_text, output_text, label) VALUES (?, ?, ?)",
            (input_text, output_text, label)
        )
        self.conn.commit()

    def fetch_similar(self, query_text: str, limit: int = 3):
        # In a real heavy production system, we would vector search these.
        # For this resume project (and Use Case 2 logic), we can do a simple text search 
        # or just return the most recent relevant ones. 
        # Enhancing this to Vector Search later is a great "Next Step".
        
        # Simple implementation: Return examples that match the label or all if no label logic yet
        # For now, let's just return the last few examples to simulate context.
        # 'Searching' logic would typically go here using embeddings.
        
        self.cursor.execute("SELECT input_text, output_text, label FROM episodes ORDER BY id DESC LIMIT ?", (limit,))
        rows = self.cursor.fetchall()
        
        examples = []
        for r in rows:
            examples.append({
                "input": r[0],
                "output": r[1],
                "label": r[2]
            })
        return examples

    def get_all_examples(self):
        self.cursor.execute("SELECT input_text, output_text, label FROM episodes")
        return [{"input": r[0], "output": r[1], "label": r[2]} for r in self.cursor.fetchall()]
