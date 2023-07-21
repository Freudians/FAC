#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

import argparse
from .vuln_module.RoleViolation import detector
from .reviser.revision import revise

#parse arguments
#returns a dictionary
def parse_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Path to the target solidity file")
    parser.add_argument("--no_revise", help="simply print the exploit instead of testing it", action="store_true")
    args = parser.parse_args()
    return args

#fyi the only arg is the filename - which has to be the source directory
def main() :
    #first parse the path
    args = parse_args()
    with open(args.filename, "r") as src :
        smart_contract = src.read()
    exploit = detector(smart_contract)
    if not args.no_revise :
        exploit = revise(smart_contract, exploit)
    with open("exploit.sol", "w") as file :
        file.write(exploit)

main()