# Email-Assistant: Self-Evolving Support Agent 🧠

> **An Advanced AI Project merging Agentic RAG with Self-Improving Memory Systems.**

## 📖 Overview
**Email-Assistant** is an autonomous support agent designed to simulate a senior support engineer. Unlike traditional RAG systems that are stateless and often repetitive, Email-Assistant **learns from experience**.

It combines two powerful AI paradigms:
1.  **Agentic RAG (Retrieval-Augmented Generation)**: Capable of researching documentation, grading its own retrieval, and self-correcting if it finds irrelevant information.
2.  **Advanced Memory Systems**:
    -   **Episodic Memory**: Remembers past similar tickets to avoid re-researching solved problems.
    -   **Procedural Memory**: Updates its own system prompts based on feedback (e.g., "Learn that API 404 errors need a specific check").
    -   **Semantic Memory**: Maintains user profiles to personalize responses.

**Built entirely on Open Source & Free Tier technologies.**

## 🏗️ Architecture

The system is orchestrated using **LangGraph**, treating the flow as a state machine.

### High-Level Logic Flow

```mermaid
graph TD
    User([User Query]) --> Triage{Triage Decision}
    
    subgraph "Memory-Based Fast Path"
        Triage -- "Known Issue" --> Context[Load Context]
        Context --> Semantic[Apply User Profile]
        Semantic --> Response
    end
    
    subgraph "Agentic RAG Path (Deep Dive)"
        Triage -- "Unknown/Complex" --> Retrieve[Retrieve Docs]
        Retrieve --> Grade{Grade Relevance}
        Grade -- "Relevant" --> Response[Synthesize Answer]
        Grade -- "Irrelevant" --> Rewrite[Rewrite Query]
        Rewrite --> Retrieve
    end
    
    Response --> Output([Final Answer])
    
    %% Learning Loop
    Output -.-> Feedback{User Feedback}
    Feedback -- "Improvement Needed" --> Optimize[Optimizer Node]
    Optimize --> UpdatePrompts[(Update System Prompts)]
```

### Component Architecture

```mermaid
classDiagram
    direction TB
    class AgentState {
        +str input
        +str decision
        +List documents
        +str feedback
    }

    class MemorySystem {
        +EpisodicMemory (SQLite)
        +ProceduralMemory (Prompts)
        +SemanticMemory (JSON)
    }

    class RAGEngine {
        +LocalVectorStore (ChromaDB)
        +DocumentGrader (Ollama)
    }

    class Orchestrator {
        +LangGraph Workflow
        +Triage Node
        +Research Node
    }

    Orchestrator --> AgentState : Manages
    Orchestrator --> MemorySystem : Queries/Updates
    Orchestrator --> RAGEngine : Delegates Research
```

## 🛠️ Tech Stack
-   **Orchestration**: [LangChain](https://python.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)
-   **LLM Runtime**: [Ollama](https://ollama.com/) (Llama 3 / Mistral)
-   **Vector Store**: [ChromaDB](https://www.trychroma.com/) (Local)
-   **Database**: SQLite (for interaction history)
-   **Language**: Python 3.10+

## 🚀 Getting Started

### Prerequisites
1.  **Python 3.10+**
2.  **Ollama** installed and running (`ollama serve`).
3.  Pull the model: `ollama pull llama3`

### Installation
```bash
# Clone the repository
git clone https://github.com/MedAzizAydi080/Email-Assistant.git
cd Email-Assistant

# Install dependencies
pip install -r requirements.txt

# Setup Scaffolding
python structure_setup.py

# Run the Agent
python main.py
```

## 🧠 Memory Data Structure
-   `data/memory/episodes.db`: Stores "few-shot" examples of past successful tickets.
-   `data/prompts/`: Text files containing system prompts.
