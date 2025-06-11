# book_translator_project/setup.py
from src.pdf_loader import load_and_chunk_pdf
from src.vector_store import create_vector_store

def setup_vector_store(pdf_path: str, store_path: str):
    """One-time setup for vector store creation"""
    chunks = load_and_chunk_pdf(pdf_path)
    vector_store = create_vector_store(chunks, "sentence-transformers/all-MiniLM-L6-v2")
    vector_store.save_local(store_path)
    print(f"Vector store created at {store_path}")

if __name__ == "__main__":
    # Example usage
    setup_vector_store("data/example_book.pdf", "data/vector_store")