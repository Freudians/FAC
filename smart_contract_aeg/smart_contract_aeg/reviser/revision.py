#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

"""
Module takes a test and a smart contract, revises the test until it works
"""
from ..config import Config
import re
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from ..Runner.runner import run_test

def revise(contract, test, setup) :
    # set up an LLM chain for revisions
    llm = ChatOpenAI(model_name=Config.model, temperature=0)
    prompt_template = """
    A programmer wrote a test that is intended to break the access
    control system of the target smart contract. When run, the
    test fails, with the following debug output. Modify the test smart contract,
    to the best of your ability, so that it works. Output the test smart
    contract. The only additional requirements are that there are at
    least 3 functions in the final test contract:
    1] A constructor, which takes no arguments
    2] A function called "setUp", which deploys an instance of the target contract. The exploit will use this instance of the target contract.
    Make sure that the exploit contract is not considered a privileged user by the target contract. If the deployment process of the target contract
    forces the exploit to be recognized as a privilege user, make sure you remove your privileges.
    3] A function called "test_exploit", which should break the access
    control of the target smart contract by elevating the privileges
    of the exploit contract. By the end of this function, the
    exploit contract should be recognized as a privileged user. Call only the functions necessary to achieve your goal. To verify
    that the explain works, call ONE privileged function at the end of the test_exploit function. Your only goal is to break
    the access control of the target smart contract: nothing more, nothing less.

    Explanation of access control vulnerabilities:
    Smart contracts often implement access control systems in order to ensure that critical functionality is unable to be accessed by untrusted users.
    These access control systems assign certain roles to certain users (represented by their address). A myriad number of methods
    can be used to keep track of these roles. Oftentimes, smart contracts will check if the calling address has a certain role before
    executing critical code that could significantly alter the behavior, monetary balance, or state of the smart contract. If the 
    calling address doesn't have the requisite role, then it cannot access the critical code. If the address/user tries to access the critical
    operations/code, then the smart contract will simply revert.

    Find the failed line the revised test/exploit. Analyze the lines around it, determine why it failed, and change the code to work.
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
        output = run_test(contract, exploit, setup)
        print(output)
        if output == "success" :
            return exploit
        args = {"exploit" : exploit, "source" : contract, "debug_msg" : output}
        unparsed_output = llm_chain(args)
        exploit = unparsed_output["text"]

