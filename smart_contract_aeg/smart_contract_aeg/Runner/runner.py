"""
Given a smart contract and exploit code, module runs it and records feedback
"""
import subprocess
import os
import shutil
from brownie import project, exceptions, network, accounts, history
import re

def run_test(target, exploit, setup) :
    """
    runs the exploit against a smart contract
    target - source of the target smart contract
    exploit - the exploit smart contract
    setup - the smart contract responsible for setting it up
    returns a string - if successful, string will be "success"
    if unsuccessful, string will represent failure
    """
    #create a project directory and copy over files
    subprocess.run("brownie init test_dir", shell=True)
    with open("test_dir/contracts/target.sol", "w") as file :
        file.write(target)
    with open("test_dir/contracts/exploit.sol", "w") as file :
        file.write(exploit)
    with open("test_dir/contracts/setup.sol", "w") as file :
        file.write(setup)
    err = ""
    try :
        # load project and connect to dev network
        proj = project.load("test_dir")
        proj.load_config()
    except exceptions.CompilerError as compile_err :
        err = str(compile_err)
        shutil.rmtree("test_dir")
        return err
    network.connect("development")
    try:
        #first deploy
        deployer = proj.Deployer.deploy({'from': accounts[0]})
        target_addr = (deployer.setup()).return_value
        exploit = proj.Exploit.deploy(target_addr, {'from': accounts[1]})
        exploit.test_exploit()
    except exceptions.VirtualMachineError as evm_err :
        failed_tx = history[-1]
        err_str = failed_tx._error_string(pad=0)
        # remove color formatting
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        err_parsed = ansi_escape.sub('', err_str)
        # format it
        err = 'Transaction failed with revert message %s \n %s' % (evm_err.revert_msg, err_parsed)
    finally :
        network.disconnect()
        proj.close()
        shutil.rmtree("test_dir")
    if err :
        return err
    else :
        return "success"