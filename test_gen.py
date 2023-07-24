#!/home/anthonyd/smartcontracts/newtool/pet_proj_env/bin/python3

from smart_contract_aeg.smart_contract_aeg.Runner.setup import *
from smart_contract_aeg.smart_contract_aeg.utils import gen_desc
import argparse

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
    desc = gen_desc(smart_contract)
    print(desc)

main()