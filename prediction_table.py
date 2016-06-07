# -*- coding: utf-8 -*
# Filename: prediction_table.py

__author__ = 'Piratf'

from grammar import Grammar
from config import Config

class PredictionTable(object):
    """the to dimensional sheet to analyze grammar"""
    def __init__(self, sheet):
        super(PredictionTable, self).__init__()
        self.sheet = sheet

    def init_sheet(self, grammar):
        string_set = set()
        name_list = [reg.name for reg in grammar.regs]
        [[string_set.update(reg.first), string_set.update(reg.follow)] for reg in grammar.regs]
        # print ("string set = ")
        # print (string_set)
        # pretreatment table
        self.sheet = [[[] for x in range(len(string_set) + 1)] for x in range(len(name_list) + 1)]
        print (len(self.sheet))
        terminator_dict = {value : index for index, value in enumerate(sorted(string_set))}
        name_dict = {value : index for index, value in enumerate(name_list)}
        for k, v in terminator_dict.items():
            self.sheet[0][v + 1].append(k)
        for k, v in name_dict.items():
            self.sheet[v + 1][0].append(k)


        for reg in grammar.regs:
            row = name_dict[reg.name] + 1
            for content in reg.contents:
                for string in content:
                    pass
            for v in reg.first:
                print ("v =", v)
                self.sheet[row][terminator_dict[v] + 1].append(v)
            if Config.null in reg.first:
                for v in reg.follow:
                    self.sheet[row][terminator_dict[v] + 1].append(v)

        self.display()

    def display(self):
        for row in self.sheet:
            for part in row:
                string = '[' + ' '.join(part) + ']'
                print (string, end = ' ')
                [print (' ', end = '') for x in range(20 - len(string))]
            print ()