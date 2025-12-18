import os

def create_structure():
    dirs = [
        "data/docs",
        "data/memory",
        "data/prompts",
        "src/memory",
        "src/rag",
        "scripts"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Create __init__.py in src subdirs
        if d.startswith("src"):
            with open(os.path.join(d, "__init__.py"), "w") as f:
                pass
                
    files = [
        "src/__init__.py",
        "src/config.py",
        "src/state.py",
        "src/graph.py",
        "main.py",
        "requirements.txt"
    ]
    
    for f in files:
        if not os.path.exists(f):
            with open(f, "w") as file:
                pass

    print(f"Project structure created in {os.getcwd()}")

if __name__ == "__main__":
    create_structure()
