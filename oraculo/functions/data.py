from datasets import load_dataset 
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import HuggingFaceDatasetLoader

from langchain.vectorstores import Chroma

def embed_text(text):
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return sentence_transformer_ef(text)


def get_dummy_dataset():
    data = load_dataset(
    "jamescalam/youtube-transcriptions",
    split="train",
    revision="8dca835"
)
    return data


def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap  = 30,
    length_function = len,
    )
    
    return splitter.create_documents([text])


def embed_documents(documents : str | list[str]):
    if isinstance(documents, str):
        return embed_text(documents)
    else:
        return [embed_text(doc) for doc in documents]


