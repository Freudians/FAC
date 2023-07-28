from ..config import Config
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ..utils import contract_to_retriever

def gen_setup_func(contract) :
    """
    Generates a function (written in solidity) that deploys a smart contract.
    takes the source of a smart contract
    returns a function that setups up the smart contract to be functional
    """
    contract_desc = gen_desc(contract)
    llm = ChatOpenAI(model_name=Config.model, temperature=0)
    prompt_template = """
    {contract}
    You are part of a team that is writing tests for a smart contract. Read through my directions carefully.
    Create a smart contract called "Deployer".
    Write a function called "setup", in solidity (the same version as the provided contract), that takes no arguments, and deploys the provided smart contract so that it can
    be used properly in accordance with its description. Once deployed, users should be able to interact with the contract in the following ways:
    {desc}
    The setup function is not part of the provided smart contract. Rather,
    it will be added to a smart contract testing suite and used to deploy this smart contract so that we can run other tests against it.
    The setup function should return the address of the deployed smart contract.
    Only output the "setup" function. Do not make ANY modifications to the code
    of the provided smart contract. Do not output the provided smart contract. Your task is not to modify the provided smart contract.
    At the top of the smart contract you output, include the line import "./target.sol". The smart contract provided will be named "target.sol". Be
    sure to also include a version pragma at the top as well.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    gen_setup_llm = LLMChain(llm=llm, prompt=prompt)
    output = gen_setup_llm({"desc" : contract_desc, "contract" : contract})
    return output["text"]

def gen_multi_setup_func(contracts) :
    """
    Generates a function (written in solidity) that deploys a smart contract ecosystem
    """
    contract_desc = gen_desc(contracts)
    llm = ChatOpenAI(model_name=Config.model, temperature=0)
    prompt_template = """
    {contracts}
    You are part of a team that is writing tests for a smart contract application. Read through my directions carefully.
    Create a smart contract called "Deployer".
    Write a function called "setup", in solidity (the same version as the provided contract), that takes no arguments, and deploys the provided smart contract so that it can
    be used properly in accordance with its description. Once deployed, users should be able to interact with the contract in the following ways:
    {desc}
    The setup function is not part of the provided smart contract. Rather,
    it will be added to a smart contract testing suite and used to deploy this smart contract application so that we can run other tests against it.
    The setup function should return the address of the deployed smart contract.
    Only output the "setup" function. Do not make ANY modifications to the code
    of the provided smart contracts. Do not output the provided smart contracts. Your task is not to modify the provided smart contracts.
    Import these files as needed in the code that you output
    """
    prompt = PromptTemplate.from_template(prompt_template)
    gen_setup_llm = LLMChain(llm=llm, prompt=prompt)
    output = gen_setup_llm({"desc" : contract_desc, "contract" : contracts})
    return output["text"]
def gen_desc(contract) :
    """
    generates a detailed description of a smart contract
    takes the source of a smart contract as a string
    returns the description (as a string)
    """
    llm = ChatOpenAI(model_name=Config.model, temperature=0)
    prompt_template = """
    {contract}
    How should this set of smart contracts function under normal usage? Explain what the intent of the contract is,
    and what other nodes on the blockchain should be able to use it to do.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    desc_gen_llm = LLMChain(llm=llm, prompt=prompt)
    result = desc_gen_llm({"contract" : contract})
    return result["text"]