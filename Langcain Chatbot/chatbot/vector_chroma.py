from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_vector_store():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(embedding_function=embeddings)
    return vector_store
