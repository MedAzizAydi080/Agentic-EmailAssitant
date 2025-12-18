from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
import operator

def merge_docs(d1: List[Document], d2: List[Document]) -> List[Document]:
    return d1 + d2

class AgentState(TypedDict):
    input: str
    chat_history: Annotated[List[BaseMessage], operator.add]
    decision: str # 'respond', 'research', 'ignore'
    documents: List[Document]
    feedback: str # For the learning loop
    user_id: str
    intermediate_steps: Annotated[List[str], operator.add]
