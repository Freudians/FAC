#!/home/anthonyd/smartcontracts/newtool/pet_proj_env/bin/python3
from smart_contract_aeg.smart_contract_aeg.Runner import run_test, gen_setup_func
from smart_contract_aeg.smart_contract_aeg.vuln_module import detector
import argparse
def parse_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Path to the target solidity file")
    parser.add_argument("--no_revise", help="simply print the exploit instead of testing it", action="store_true")
    args = parser.parse_args()
    return args

def main() :
    args = parse_args()
    with open(args.filename, "r") as src :
        smart_contract = src.read()
    setup = gen_setup_func(smart_contract)
    exploit = detector(smart_contract)
    output = run_test(smart_contract, exploit, setup)
    print(output.encode('utf-8'))
main()