from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
import json

from .state import AgentState
from .config import LLM_MODEL, OLLAMA_BASE_URL
from .memory.episodic import EpisodicMemory
from .memory.procedural import ProceduralMemory
from .memory.semantic import SemanticMemory
from .rag.vectorstore import LocalVectorStore
from .rag.grader import DocumentGrader

# Initialize Components
llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
episodic_mem = EpisodicMemory()
procedural_mem = ProceduralMemory()
vector_store = LocalVectorStore() # This loads the embeddings model, might be heavy
grader = DocumentGrader()

# --- Nodes ---

def triage_node(state: AgentState):
    """Decides the path based on memory and query complexity."""
    print("--- TRIAGE NODE ---")
    query = state['input']
    user_id = state['user_id']
    
    # 1. Fetch few-shot examples from Episodic Memory
    examples = episodic_mem.fetch_similar(query)
    examples_str = "\n".join([f"Q: {e['input']}\nDecision: {e['label']}" for e in examples])
    
    # 2. Load System Prompt from Procedural Memory
    system_prompt_template = procedural_mem.load_prompt("triage")
    system_prompt = system_prompt_template.format(examples=examples_str, query=query)
    
    # 3. Call LLM for decision
    try:
        response = llm.invoke([HumanMessage(content=system_prompt)])
        # Expert handling of potentially messy JSON output from smaller local models
        content = response.content.replace("```json", "").replace("```", "").strip()
        decision_data = json.loads(content)
        decision = decision_data.get("decision", "research")
    except Exception as e:
        print(f"Triage JSON parse error: {e}. Defaulting to 'research'")
        decision = "research"
        
    return {"decision": decision}

def research_node(state: AgentState):
    """Performs Agentic RAG."""
    print("--- RESEARCH NODE ---")
    query = state['input']
    
    # 1. Retrieve
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(query)
    
    # 2. Grade
    relevant_docs = []
    for doc in docs:
        score = grader.grade(question=query, context=doc.page_content)
        if score == "yes":
            relevant_docs.append(doc)
            
    if not relevant_docs:
        # Simple self-correction for this demo:
        # If no docs found, try a broader query (naive implementation)
        print("No relevant docs found. Trying broader search...")
        # (In a full implementation, we would have a rewrite_node here)
        
    return {"documents": relevant_docs}

def response_node(state: AgentState):
    """Synthesizes the final answer."""
    print("--- RESPONSE NODE ---")
    query = state['input']
    docs = state.get('documents', [])
    user_id = state['user_id']
    
    # 1. Load User Profile (Semantic Memory)
    semantic_mem = SemanticMemory(user_id)
    user_context = semantic_mem.get_context_str()
    
    # 2. Format Context from Docs
    context_str = "\n\n".join([d.page_content for d in docs])
    
    # 3. Load Prompt
    prompt_template = procedural_mem.load_prompt("response")
    final_prompt = prompt_template.format(context=context_str, query=query)
    
    # 4. Generate
    messages = [
        SystemMessage(content=f"User Context: {user_context}"),
        HumanMessage(content=final_prompt)
    ]
    response = llm.invoke(messages)
    
    return {"chat_history": [AIMessage(content=response.content)]}

def feedback_learning_node(state: AgentState):
    """Mock node to simulate learning from feedback."""
    print("--- LEARNING NODE ---")
    # This would take state['feedback'] and call procedural_mem.update_prompt
    # For now, just a pass-through
    return {}

# --- Graph Construction ---

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("triage", triage_node)
    workflow.add_node("research", research_node)
    workflow.add_node("response", response_node)
    # workflow.add_node("learn", feedback_learning_node) 
    
    workflow.add_edge(START, "triage")
    
    def route_decision(state):
        if state["decision"] == "research":
            return "research"
        elif state["decision"] == "respond":
            return "response" # Skip RAG, go straight to response (using internal knowledge)
        else:
            return "response" # Default fallback
            
    workflow.add_conditional_edges("triage", route_decision)
    
    workflow.add_edge("research", "response")
    workflow.add_edge("response", END)
    
    return workflow.compile()
