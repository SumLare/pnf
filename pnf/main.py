# -*- coding: utf-8 -*-
import re

def main():
    formula = input("Transform your formula to PNF: ")
    while formula:
        parse(formula)
        formula = input("Transform your formula to PNF: ")

def eliminate_implication(formula):
    statements = formula.split("->")
    statements[0] = "~" + statements[:2][0].strip()
    first_two = " |".join(statements[:2])
    return first_two + "->{0}".format(''.join(statements[2:]))

def inward_negation(formula):
    index = formula.find("~∃") if formula.find("~∃") is not -1 else formula.find("~∀")
    while index is not -1:
        replace_index = index + 2
        newformula = formula[:index] + formula[(index+1):]
        formula = newformula[:replace_index] + "~" + newformula[replace_index:]
        index = formula.find("~∃") if formula.find("~∃") is not -1 else formula.find("~∀")
    return re.sub("~~", "", formula)

def parse(formula):
    if "->" in formula: formula = eliminate_implication(formula)
    if "~" in formula: formula = inward_negation(formula)
    return print(formula)

if __name__ == '__main__':
    main()
