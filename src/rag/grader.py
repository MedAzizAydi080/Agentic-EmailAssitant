from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from ..config import LLM_MODEL, OLLAMA_BASE_URL

# Structured Output for Grading
class GradeDocuments(BaseModel):
    """Binary score for relevance check."""
    binary_score: str = Field(description="Relevance score 'yes' or 'no'")

class DocumentGrader:
    def __init__(self):
        self.llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        self.structured_llm = self.llm.with_structured_output(GradeDocuments)
        
        self.prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved document to a user question.
            
            Retrieved document: 
            {context}
            
            User Question: 
            {question}
            
            If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
            Give a binary score 'yes' or 'no'.
            """,
            input_variables=["question", "context"]
        )
        self.chain = self.prompt | self.structured_llm

    def grade(self, question: str, context: str) -> str:
        try:
            result = self.chain.invoke({"question": question, "context": context})
            return result.binary_score
        except Exception as e:
            # Fallback if structured output fails on local model (common issue)
            print(f"Grading error: {e}. Defaulting to 'yes'")
            return "yes"
