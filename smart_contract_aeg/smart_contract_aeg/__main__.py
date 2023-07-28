#!/home/anthonyd/smartcontracts/newtool/pet_proj/env/bin/python3

import argparse
from .exploit_gen.RoleViolation import role_violation
from .reviser.revision import revise
from .Runner.setup import gen_setup_func

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
    setup = gen_setup_func(smart_contract)
    exploit = role_violation(smart_contract)
    if not args.no_revise :
        exploit = revise(smart_contract, exploit, setup)
    with open("exploit.sol", "w") as file :
        file.write(exploit)

main()