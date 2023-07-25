#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

""""
Module detects access control role violations. This is when an unauthorized user can obtain a higher privileged role
"""
from ..config import *
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

def detector(contract) :
    """"
    takes the source code of a smart contract as an argument
    returns a POC access control exploit
    """
    llm = ChatOpenAI(model_name=model, temperature=0)
    prompt_template= """
    You are a programmer tasked with writing tests for the access control system defined in the smart contract included. 
    I will refer to the provided smart contract as "Zaima".
    Write a smart contract, in solidity (same version as Zaima) that breaks the access control of Zaima. 
    The smart contract should be called "Exploit". It should include at least 3 functions:
    1] A constructor, which takes a single argument - the address of the target smart contract 
    2] A fallback function to receive payment
    3] A function called "test_exploit", which should break the access control of Zaima. Identify the access control system implemented in the smart contract, and then
    break it by elevating the privileges of the exploit contract. By the end of the "exploit" function, the Exploit smart contract should be recognized
    as a privileged user.
    Include comments explaining how each line of code in the exploit function breaks the access control of Zaima. Do your best to only make
    successful function calls. Bear in mind that "Zaima" is not the actual name of the smart contract, and you should not refer to the smart contract
    as "Zaima" in the code you produce. Call only the functions necessary to achieve your goal. To verify
    that the explain works, call ONE privileged function at the end of the test_exploit function. Your only goal is to break
    the access control of Zaima : nothing more, nothing less. Be sure to use the actual name of the target smart contract in your code.

    Feel free to include extra functions that are necessary to achieve your goal, but don't expect them to be called.
    At the top of the program you output, have a pragma statement specifying the solidity version, and import the contract loacted at "./target.sol"
    The exploit contract you write may depend on code defined in other smart contracts, in particular, the exploit contract.
    However, you should not include the code of any of these dependencies in the output. Only output the exploit contract, and nothing further. 

    Smart contracts often implement access control systems in order to ensure that critical functionality is unable to be accessed by untrusted users.
    These access control systems assign certain roles to certain users (represented by their address). A myriad number of methods
    can be used to keep track of these roles. Oftentimes, smart contracts will check if the calling address has a certain role before
    executing critical code that could significantly alter the behavior, monetary balance, or state of the smart contract. If the 
    calling address doesn't have the requisite role, then it cannot access the critical code. If the address/user tries to access the critical
    operations/code, then the smart contract will simply revert.
    Here's the smart contract: 
    {source}
    
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["source"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain(contract)
    return response["text"]