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

    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["source", "exploit", "debug_msg"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    while True :
        output = run_test(contract, test)
        