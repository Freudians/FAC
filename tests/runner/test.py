#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3
import sys
sys.path.append("/home/anthonyd/smartcontracts/newtool/pet_proj/src")
import Runner.runner as runner

def compiler_err() :
    target_file = open("tests/runner/contracts/target.sol")
    target = target_file.read()
    exploit_file = open("tests/runner/contracts/compiler_error.sol")
    exploit = exploit_file.read()
    output = runner.run_test(target, exploit)
    print("it failed\n" + output["feedback"])

def runtime_err() :
    target_file = open("tests/runner/contracts/target.sol")
    target = target_file.read()
    exploit_file = open("tests/runner/contracts/runtime_error.sol")
    exploit = exploit_file.read()
    output = runner.run_test(target, exploit)
    print("it failed\n" + output["feedback"])

runtime_err()