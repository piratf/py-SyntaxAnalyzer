# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from reg import Reg
from grammar import Grammar
import sys

separator_str = '::='
split_str = '|'

# read config file
def config():
    with open('config.conf') as conf:
        line = conf.readline()
        separator_str = line.split('=')[1].strip()
        line = conf.readline()
        split_str = line.split('=')[1].strip()

# read regs from file
def readGrammar():
    regs = []
    with open('input.txt') as input:
        lines = input.readlines();
        for line in lines:
            name, content = [x.strip() for x in line.split(separator_str)]
            contents = [x.strip() for x in content.split(split_str)]
            regs.append(Reg(name, contents))
    return Grammar(regs)

if __name__ == "__main__":
    config()
    grammar = readGrammar()
    # grammar.remove_direct_left_recursion()
    grammar.remove_indirect_left_recursion()
    sys.stdout = open("output.txt", "w")
    grammar.display()
    sys.stdout = sys.__stdout__

    