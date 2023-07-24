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

def gen_desc(contract) :
    """
    generates a detailed description of a smart contract
    takes the source of a smart contract as a string
    returns the description (as a string)
    """
    llm = ChatOpenAI(model_name=model, temperature=0)
    prompt_template = """
    You are writing detailed documentation for a smart contract. Describe, in great detail, how the smart contract should be able to be used.

    Here is the source file. It may contain multiple smart contracts, but focus on the main one:
    {contract}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    desc_gen_llm = LLMChain(llm=llm, prompt=prompt)
    result = desc_gen_llm({"contract" : contract})
    return result["text"]