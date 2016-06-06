# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from reg import Reg
from grammar import Grammar
from config import Config
import sys

# read regs from file
def readGrammar():
    regs = []
    with open('g3.4.txt') as input:
        lines = input.readlines();
        for line in lines:
            name, content = [x.strip() for x in line.split(Config.separator_str)]
            content_string = [x.strip() for x in content.split(Config.split_str)]
            contents = []
            for content in content_string:
                contents.append([x for x in [c.strip() for c in content.split(' ')]])
            regs.append(Reg(name, contents))
    return Grammar(regs)

if __name__ == "__main__":
    Config.read_config()
    grammar = readGrammar()
    sys.stdout = open("output.txt", "w")
    grammar.display()
    # grammar.remove_direct_left_recursion()
    grammar.remove_indirect_left_recursion()
    # grammar.extract_left_factor()
    # grammar.get_first_set()
    grammar.display()
    sys.stdout = sys.__stdout__

    