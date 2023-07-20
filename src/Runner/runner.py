"""
Given a smart contract and exploit code, module runs it and records feedback
"""
from brownie.exceptions import *
from brownie.project import compile_source
import brownie.network as network
from brownie.network import accounts
import brownie
import subprocess

def run_test(target, exploit) :
    """
    runs the exploit against a smart contract
    takes the source of the target and the source of the exploit - both solidity strings
    """
    network.connect("development")
    parsed_exploit = [s for s in exploit.split("\n") if not "pragma" in s]
    combined_contract = target + "\n".join(parsed_exploit)
    output = { "success" : True, "feedback" : "", "Error_type" : ""}
    try:
        pro = compile_source(combined_contract)
    except CompilerError as err :
        output["success"] = False
        output["Error_type"] = "compiler"
        output["feedback"] = str(err)
        return output
    exploit_inst = pro.Exploit.deploy({"from": accounts[0]})
    try:
        setup_tx = exploit_inst.setup()
        exploit_tx = exploit_inst.exploit()
    except VirtualMachineError as err :
        output["success"] = False
        output["Error_type"] = "runtime"
        hist = network.TxHistory()
        tx = hist[-1]
        failed_instruction = tx.trace[-1]
        output["feedback"] = err.dev_revert_msg
        return output
    network.disconnect()
    return output
