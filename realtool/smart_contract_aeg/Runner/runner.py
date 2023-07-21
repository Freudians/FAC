"""
Given a smart contract and exploit code, module runs it and records feedback
"""
import subprocess
import os
import shutil

def run_test(target, exploit) :
    """
    runs the exploit against a smart contract
    takes the source of the target and the source of the exploit - both solidity strings
    """
    #copy the program over to forge
    print(os.getcwd())
    subprocess.run("forge init --no-commit --force test_dir", shell=True)
    with open("test_dir/test/exploit.sol", "w") as file :
        file.write(exploit)
    with open("test_dir/src/target.sol", "w") as file :
        file.write(target)
    #delete extra stuff
    if os.path.exists("test_dir/src/Counter.sol") :
        os.remove("test_dir/src/Counter.sol")
    if os.path.exists("test_dir/test/Counter.t.sol") :
        os.remove("test_dir/test/Counter.t.sol")
    if os.path.exists("test_dir/script/Counter.s.sol") :
        os.remove("test_dir/script/Counter.s.sol")
    os.chdir("test_dir")
    #actually run the test
    test_result = subprocess.run("forge test -vvv", shell=True, capture_output=True, encoding="utf-8")
    #cleanup
    os.chdir("..")
    shutil.rmtree("test_dir")
    #return result
    if "FAIL" in test_result.stdout :
        return test_result.stdout
    if test_result.stderr :
       return test_result.stderr 
    else :
        return "success"
