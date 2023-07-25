from ..utils import gen_desc
from ..config import *
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def gen_setup_func(contract) :
    """
    Generates a function (written in solidity) that deploys a smart contract.
    takes the source of a smart contract
    returns a function that setups up the smart contract to be functional
    """
    contract_desc = gen_desc(contract)
    llm = ChatOpenAI(model_name=model, temperature=0)
    prompt_template = """
    {contract}
    You are part of a team that is writing tests for a smart contract. Read through my directions carefully.
    Create a smart contract called "Deployer".
    Write a function called "setup", in solidity (the same version as the provided contract), that takes no arguments, and deploys the provided smart contract so that it can
    be used properly in accordance with its description. Deployment goes beyond any specific function calls or code actions. Sometimes, it can be as
    simple as just calling the constructor of the target contract. Other times, further actions need to be performed so that the deployed
    smart contract is usable, such as invoking further functions or sending it currency. In the setup() function, you should do whatever is necessary
    to deploy the smart contract provided, so that it can fulfill the necessary use cases.
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


