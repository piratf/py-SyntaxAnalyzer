# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from reg import Reg
from grammar import Grammar
from config import Config
import sys

separator_str = '::='
split_str = '|'

# read regs from file
def readGrammar():
    regs = []
    with open('input.txt') as input:
        lines = input.readlines();
        for line in lines:
            name, content = [x.strip() for x in line.split(Config.separator_str)]
            contents = [x.strip() for x in content.split(Config.split_str)]
            regs.append(Reg(name, contents))
    return Grammar(regs)

if __name__ == "__main__":
    Config.read_config()
    grammar = readGrammar()
    # grammar.remove_direct_left_recursion()
    grammar.remove_indirect_left_recursion()
    grammar.extract_left_factor()
    sys.stdout = open("output.txt", "w")
    grammar.display()
    sys.stdout = sys.__stdout__

    