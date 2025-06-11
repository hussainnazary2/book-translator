# book_translator_project/src/llm_query.py
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def get_qa_chain(vector_store, model_path: str):
    """Create QA chain with local LLM"""
    # In llm_query.py, update the LlamaCpp initialization:
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.1,
        max_tokens=200,
        n_ctx=32768,  # Match the model's training context size
        n_gpu_layers=20,
        verbose=False,
    )
    prompt_template = """
    <s>[INST] Use the following context to answer the question at the end.
    If you don't know the answer, just say you don't know.

    Context: {context}

    Question: {question} [/INST]
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )