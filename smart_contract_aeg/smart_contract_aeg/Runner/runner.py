"""
Given a smart contract and exploit code, module runs it and records feedback
"""
import subprocess
import os
import shutil
from brownie import project, exceptions, network, accounts

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
    try :
        # load project and connect to dev network
        proj = project.load("test_dir")
        proj.load_config()
        network.connect('development')
        #first deploy
        deployer = proj.Deployer.deploy({'from': accounts[0]})
        target_addr = (deployer.setup()).return_value
        exploit = proj.Exploit.deploy(target_addr, {'from': accounts[1]})
        exploit.test_exploit()
    except exceptions.CompilerError as compile_err :
        return str(compile_err)
    # clean up 
    network.disconnect()
    #shutil.rmtree("test_dir")
    return "success"