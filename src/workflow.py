# book_translator_project/src/workflow.py
from typing import TypedDict
from langgraph.graph import StateGraph, END
from .translator import Translator
from .llm_query import get_qa_chain
from .vector_store import load_vector_store

# Define state structure
class GraphState(TypedDict):
    question_fa: str
    question_en: str
    context: str
    answer_en: str
    answer_fa: str

# Initialize models and components
fa_en_translator = Translator("models/fa_en")  # NOT models/mt5-fa-en
en_fa_translator = Translator("models/en_fa")  # This matches your folder
vector_store = load_vector_store("data/vector_store", "sentence-transformers/all-MiniLM-L6-v2")
qa_chain = get_qa_chain(vector_store, "models/Mistral-7B-Instruct.gguf")

def translate_fa_to_en(state: GraphState):
    """Translate Persian question to English"""
    return {"question_en": fa_en_translator.translate(state["question_fa"])}

def retrieve_context(state: GraphState):
    """Retrieve relevant context from vector store"""
    result = qa_chain.invoke({"query": state["question_en"]})
    return {"context": result["source_documents"], "answer_en": result["result"]}

def translate_en_to_fa(state: GraphState):
    """Translate English answer to Persian"""
    return {"answer_fa": en_fa_translator.translate(state["answer_en"])}

def final_answer(state: GraphState):
    """Return final Persian answer"""
    return state["answer_fa"]

# Build the workflow graph
workflow = StateGraph(GraphState)

# Define nodes
workflow.add_node("translate_fa_to_en", translate_fa_to_en)
workflow.add_node("retrieve_context", retrieve_context)
workflow.add_node("translate_en_to_fa", translate_en_to_fa)
workflow.add_node("final_answer", final_answer)

# Define edges
workflow.set_entry_point("translate_fa_to_en")
workflow.add_edge("translate_fa_to_en", "retrieve_context")
workflow.add_edge("retrieve_context", "translate_en_to_fa")
workflow.add_edge("translate_en_to_fa", "final_answer")
workflow.add_edge("final_answer", END)

# Compile the graph
app = workflow.compile()

# Main function to execute the workflow
def run_qa(question_fa: str) -> str:
    """Run Persian QA workflow end-to-end"""
    result = app.invoke({"question_fa": question_fa})
    return result