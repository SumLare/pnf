# -*- coding: utf-8 -*-
import re
import string
import random

def main():
    formula = input("Transform your formula to PNF: ")
    while formula:
        parse(formula)
        formula = input("Transform your formula to PNF: ")

def eliminate_equivalence(formula):
    statements = formula.split("<->")
    left_literal = "(~" + statements[0].strip() + " | " + statements[1].strip() + ")"
    right_literal = "(" + statements[0].strip() + " | ~" + statements[1].strip() + ")"
    return " & ".join([left_literal, right_literal])

def eliminate_implication(formula):
    statements_in_params = re.findall("\((.*?)\)", formula)
    if "->" in statements_in_params:statements = formula.split("->")
    for statement in statements_in_params:
        if "->" in statement:
            statements = statement.split("->")
            statements[0] = "~" + statements[:2][0].strip()
        else
            statements = formula.split("->")
    return " |".join(statements[:2])

def inward_negation(formula):
    if formula.find("~∃") is not -1: raise SyntaxError("Use parentheses with quantifiers")
    index = formula.find("~(∃") if formula.find("~(∃") is not -1 else formula.find("~(∀")
    while index is not -1:
        replace_index = index + 2
        without_negation = formula[:index] + formula[index+2:]
        literal = without_negation[:index] + without_negation[index+1:]
        formula = literal[:index] + "(" + change_quantifier(without_negation[index]) + \
                  literal[index:replace_index] + "~" + literal[replace_index:]
        index = formula.find("~(∃") if formula.find("~(∃") is not -1 else formula.find("~(∀")
    return re.sub("~~", "", formula)

def change_quantifier(quantifier):
    if quantifier == "∃":
        return re.sub("∃", "∀", quantifier)
    else:
        return re.sub("∀", "∃", quantifier)

def standardize(formula):
    quantifier_pattern = re.compile("∀|∃")
    quantifier_indexes = [q.start(0) for q in quantifier_pattern.finditer(formula)]
    for q_index in quantifier_indexes:
        new_var = random.choice(string.ascii_letters[:26])
        if formula[q_index+2] == "(":
            close_parant_index = formula[q_index:].index(")")
            literal_in_parant = formula[q_index:][3:close_parant_index]
            changed_literal_in_parant = re.sub(r"[a-z]", new_var, literal_in_parant)
            return formula[:q_index+1] + new_var + "(" + changed_literal_in_parant + formula[q_index:][close_parant_index:]
        else:
            return formula[:q_index+1] + new_var + formula[q_index+2] + new_var + formula[q_index+4:]

def parse(formula):
    if "<->" in formula: formula = eliminate_equivalence(formula)
    if "->" in formula: formula = eliminate_implication(formula)
    if "~" in formula: formula = inward_negation(formula)
    formula = standardize(formula)
    return print(formula)

if __name__ == '__main__':
    main()
