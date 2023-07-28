#!/home/anthonyd/smartcontracts/newtool/pet_proj_env/bin/python3
from smart_contract_aeg.smart_contract_aeg.Runner import run_test, gen_setup_func
from smart_contract_aeg.smart_contract_aeg.exploit_gen import detector
from smart_contract_aeg.smart_contract_aeg.reviser import revise
import argparse
def parse_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help="Path to the target solidity file")
    parser.add_argument('exploit', help="Path to the exploit file")
    parser.add_argument('setup', help="path to the setup file")
    parser.add_argument("--no_revise", help="simply print the exploit instead of testing it", action="store_true")
    args = parser.parse_args()
    return args

def main() :
    args = parse_args()
    with open(args.target, "r") as src :
        target = src.read()
    with open(args.exploit, "r") as src :
        exploit = src.read()
    with open(args.setup, 'r') as src :
        setup = src.read()
    output = revise(target, exploit, setup)
    print(output)
main()