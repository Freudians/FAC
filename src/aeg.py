#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

import argparse
import vuln_module.RoleViolation as RoleViolation
from Runner.runner import run_test

#parse arguments
#returns a dictionary
def parse_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    return { 'filename' : args.filename}

#fyi the only arg is the filename - which has to be the source directory
def main() :
    #first parse the path
    args = parse_args()
    src_path = args["filename"]
    with open(src_path, "r") as src :
        smart_contract = src.read()
    exploit = RoleViolation.detector(smart_contract)
    with open("test_exploit.sol", "w") as output :
        output.write(exploit)
    outcome = run_test(smart_contract, exploit)
    if outcome["success"] :
        print("it worked")
    else :
        print("it failed")
        print(outcome["feedback"])
if __name__ == "__main__" :
    main()