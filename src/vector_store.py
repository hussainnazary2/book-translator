# book_translator_project/src/vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def create_vector_store(chunks: list[Document], embedding_model: str):
    """Create and save vector store from document chunks"""
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def load_vector_store(store_path: str, embedding_model: str):
    """Load existing vector store"""
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    return FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)