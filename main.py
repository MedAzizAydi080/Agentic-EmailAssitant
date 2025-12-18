from src.graph import build_graph
from src.state import AgentState
from src.memory.semantic import SemanticMemory
import uuid

def main():
    print("Initializing MemoRAG Agent...")
    graph = build_graph()
    
    user_id = "user_123"
    
    # Ensure user has a profile
    semantic = SemanticMemory(user_id)
    if not semantic.profile.get("name"):
        semantic.update_profile("name", "Alice")
        print("Created new user profile for Alice.")

    print("\nMemoRAG Ready! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        query = input("\nUser: ")
        if query.lower() in ["quit", "exit"]:
            break
            
        initial_state = AgentState(
            input=query,
            chat_history=[],
            decision="",
            documents=[],
            feedback="",
            user_id=user_id,
            intermediate_steps=[]
        )
        
        # Stream the graph
        print("\n[Agent Thinking...]")
        try:
            for event in graph.stream(initial_state):
                for key, value in event.items():
                    print(f"  -> Finished Step: {key}")
                    if key == "triage":
                        print(f"     Decision: {value.get('decision')}")
                    if key == "response":
                        print(f"\nAgent: {value['chat_history'][0].content}")
        except Exception as e:
            print(f"Error during execution: {e}")
            print("Tip: Ensure Ollama is running (`ollama serve`).")

if __name__ == "__main__":
    main()
