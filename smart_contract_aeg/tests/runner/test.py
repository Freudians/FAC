#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3
import sys
sys.path.append("/home/anthonyd/smartcontracts/newtool/pet_proj/src")
import Runner.runner as runner

def compiler_err() :
    target_file = open("tests/runner/contracts/target.sol")
    target = target_file.read()
    exploit_file = open("tests/runner/contracts/compiler_error.sol")
    exploit = exploit_file.read()
    runner.run_test(target, exploit)

def runtime_err() :
    target_file = open("tests/runner/contracts/target.sol")
    target = target_file.read()
    exploit_file = open("tests/runner/contracts/runtime_error.sol")
    exploit = exploit_file.read()
    output = runner.run_test(target, exploit)
    print("returned output: \n" + output)
def working() :
    target_file = open("tests/runner/contracts/target.sol")
    target = target_file.read()
    exploit_file = open("tests/runner/contracts/working.sol")
    exploit = exploit_file.read()
    output = runner.run_test(target, exploit)
    print("returned output: \n" + output)
working()