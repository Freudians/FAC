from .config import *
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from langchain.vectorstores import Chroma 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory

def contract_to_retriever(contract) :
    """
    takes a smart contract source (string) and returns a retriever over it
    """
    solidity_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.SOL, chunk_size=4000, chunk_overlap=0
    )
    docs = solidity_splitter.create_documents([contract])
    db = Chroma.from_documents(docs, OpenAIEmbeddings())
    retriever = db.as_retriever(search_kwargs={"k": 1}, )
    return retriever

def load_contracts(dir_path) :
    """
    loads all contracts from a directory into one massive string
    dir_path - path to the directory
    """
    contracts = ""
    for path, dir, files in os.walk(dir_path) :
        for src_file in files :
            if os.path.splitext(src_file)[1] != ".sol" :
                continue
            with os.open(src_file) as file :
                contracts += str(os.path.join(path, src_file))
                contracts += '\n'
                contracts += file.read()
