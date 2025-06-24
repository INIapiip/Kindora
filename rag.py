import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from google.generativeai.generative_models import GenerativeModel

def load_retriever():
    client = GenerativeModel(model_name="embedding-001")  # model khusus untuk embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001")
    db = FAISS.load_local("data/faiss_index", embeddings)
    return db.as_retriever(search_kwargs={"k": 3})

def get_rag_response(query, retriever, llm):
    qa: BaseRetrievalQA = BaseRetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    return qa({"query": query})
