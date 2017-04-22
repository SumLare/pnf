# -*- coding: utf-8 -*-
import re

def main():
    formula = input("Transform your formula to PNF: ")
    while formula:
        if "->" in formula: formula = process_implication(formula)
        if "-" in formula: formula = process_negation(formula)
        print(formula)
        formula = input("Transform your formula to PNF: ")

def process_implication(formula):
    statements = formula.split("->")
    statements[0] = "-" + statements[:2][0].strip()
    first_two = " |".join(statements[:2])
    return first_two + "->{0}".format(''.join(statements[2:]))

def process_negation(formula):
    if "--" in formula:
        return re.sub("--", "", formula)

if __name__ == '__main__':
    main()
