# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from lexical import Lexical, LexicalResult
from reg import Reg
from grammar import Grammar
from prediction_table import PredictionTable
from config import Config
import sys

# read regs from file
def readGrammar(filePath):
    regs = []
    with open(filePath) as input:
        lines = input.readlines();
        for line in lines:
            name, content = [x.strip() for x in line.split(Config.separator_str)]
            content_string = [x.strip() for x in content.split(Config.split_str)]
            contents = []
            for content in content_string:
                contents.append([x for x in [c.strip() for c in content.split(' ')] if x != Config.null])
            regs.append(Reg(name, contents))
    return Grammar(regs)

def test(filePath, ansPath=None, string=None, lexical=None):
    grammar = readGrammar(filePath)
    if ansPath != None:
        ans = readGrammar(ansPath)
    sys.stdout = open("output.txt", "w")
    # grammar.remove_direct_left_recursion(0)
    grammar.remove_indirect_left_recursion()
    grammar.extract_left_factor()
    grammar.get_first_set()
    grammar.get_follow_set()
    grammar.display()
    sheet = PredictionTable(grammar)
    sheet.display()

    if lexical is not None:
        lexical.display()
        sheet.analyze(lexical)

    if string is not None:
        sheet.analyze_string(string)
    # ans.display()
    # assert grammar == ans
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    Config.read_config()
    lr = LexicalResult()
    lr.init_from_file('result.txt', 'parseCode.txt')
    # for all the process
    test('g3.9.txt', 'g3.9`.txt', "id + id * id ;")
    # test('g3.8.txt', 'g3.8`.txt')
    # test('g3.4.txt', 'g3.4`.txt')
    # test('g3.10.txt', 'g3.10`.txt')
    # test('g3.11.txt', string = 'a b b c d e')
    test('my_test.txt', lexical=lr)
