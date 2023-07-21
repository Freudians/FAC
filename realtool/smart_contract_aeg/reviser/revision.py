#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

"""
Module takes a test and a smart contract, revises the test until it works
"""
import sys
sys.path.append("/home/anthonyd/smartcontracts/newtool/pet_proj/src")
import os
os.environ["OPENAI_API_KEY"] = "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"
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from Runner.runner import run_test

def revise(contract, test) :
    # set up an LLM chain for revisions
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
    prompt_template = """
    A programmer wrote a test that is intended to break the access
    control system of the target smart contract. When run, the
    test fails, with the following debug output. Modify the test smart contract,
    to the best of your ability, so that it works. Output the test smart
    contract. The only additional requirements are that there are at
    least 3 functions in the final test contract:
    1] A constructor, which takes no arguments
    2] A function called "setUp", which deploys an instance of the target contract. The exploit will use this instance of the target contract.
    Ensure that after the target contract is deployed, the exploit contract has not been granted any special privileges whatsoever.
    If the constructor of Zaima grants ownership to the deployer, make sure to transfer ownership to another address in the setup function.
    3] A function called "test_exploit", which should break the access
    control of the target smart contract by elevating the privileges
    of the exploit contract. By the end of this function, the
    exploit contract should be recognized as a privileged user. Invoke the minimum number of functions needed to achieve your goal. To verify
    that the explain works, call ONE privileged function at the end of the test_exploit function.

    Explanation of access control vulnerabilities:
    Smart contracts often implement access control systems in order to ensure that critical functionality is unable to be accessed by untrusted users.
    These access control systems assign certain roles to certain users (represented by their address). A myriad number of methods
    can be used to keep track of these roles. Oftentimes, smart contracts will check if the calling address has a certain role before
    executing critical code that could significantly alter the behavior, monetary balance, or state of the smart contract. If the 
    calling address doesn't have the requisite role, then it cannot access the critical code. If the address/user tries to access the critical
    operations/code, then the smart contract will simply revert.

    Target Contract:
    {source}

    Faulty test/exploit:
    {exploit}

    Debug output :
    {debug_msg}

    Output the revised test/exploit, and nothing more.
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["source", "exploit", "debug_msg"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    exploit = test
    while True :
        print(exploit)
        output = run_test(contract, exploit)
        if output == "success" :
            return exploit
        args = {"exploit" : exploit, "source" : contract, "debug_msg" : output}
        unparsed_output = llm_chain(args)
        exploit = unparsed_output["text"]
