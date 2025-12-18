import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.episodic import EpisodicMemory

def seed_episodes():
    mem = EpisodicMemory()
    
    # Examples from Use Case 2 (adapted) & Use Case 1 relevant concepts
    examples = [
        {
            "input": "From: spam@example.com\nSubject: BIG SALE!!!\nBody: Buy now!",
            "output": "ignore",
            "label": "ignore"
        },
        {
            "input": "From: boss@company.com\nSubject: Project Update\nBody: Where are we on the report?",
            "output": "respond",
            "label": "respond"
        },
        {
            "input": "From: dev@client.com\nSubject: API 404 Error\nBody: I cannot access endpoint /v1/users. Is it down?",
            "output": "research", 
            "label": "research" # This triggers the RAG flow
        },
        {
            "input": "From: alice@company.com\nSubject: Documentation missing\nBody: I can't find the docs for the new feature.",
            "output": "research",
            "label": "research"
        }
    ]
    
    print(f"Seeding {len(examples)} examples into Episodic Memory...")
    for ex in examples:
        mem.add_episode(ex["input"], ex["output"], ex["label"])
        
    print("Seeding complete.")

if __name__ == "__main__":
    seed_episodes()
