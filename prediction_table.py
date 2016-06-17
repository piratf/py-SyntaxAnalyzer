# -*- coding: utf-8 -*
# Filename: prediction_table.py

__author__ = 'Piratf'

from grammar import Grammar
from config import Config
from my_exceptions import WrongGrammar

class PredictionTable(object):
    """the to dimensional sheet to analyze grammar"""
    def __init__(self, grammar):
        super(PredictionTable, self).__init__()
        self.name_set = grammar.name_set
        self.init_sheet(grammar)

    def display(self):
        print ("========================== {} =========================".format("prediction table display"))
        for row in self.sheet:
            for part in row:
                string = '[' + ' '.join(part) + ']'
                print (string, end = ' ')
                [print (' ', end = '') for x in range(20 - len(string))]
            print ()
        print ("========================== {} =====================\n".format("prediction table display end"))


    def init_sheet(self, grammar):
        string_set = set()
        name_list = [reg.name for reg in grammar.regs]
        [[string_set.update(reg.first), string_set.update(reg.follow)] for reg in grammar.regs]
        # print ("string set = ")
        # print (string_set)
        # pretreatment table
        self.sheet = [[[] for x in range(len(string_set) + 1)] for x in range(len(name_list) + 1)]
        self.terminator_dict = {value : index + 1 for index, value in enumerate(sorted(string_set))}
        self.name_dict = {value : index + 1 for index, value in enumerate(name_list)}
        for k, v in self.terminator_dict.items():
            self.sheet[0][v].append(k)
        for k, v in self.name_dict.items():
            self.sheet[v][0].append(k)


        for reg in grammar.regs:
            row = self.name_dict[reg.name]
            for content in reg.contents:
                if content == []:
                    content = [Config.null]
                c_first = grammar.do_first_from_content(content)
                [self.sheet[row][self.terminator_dict[ter]].extend(content) for ter in c_first if ter not in self.name_set]
                if Config.null in c_first:
                    [self.sheet[row][self.terminator_dict[v]].extend(content) for v in reg.follow if v not in self.name_set]

    def analyze(self, lexical):
        print ("====================== {} =========================".format("start analyze"))
        stack = ['#', self.sheet[1][0][0]]
        cur = [c.tag for c in lexical.result_list]
        cur.append('#')

        pos = 0
        i = 0
        while not (stack[-1] == '#' and cur[pos] == '#'):
            ip = cur[pos]
            top = stack[-1]
            print ("top =", top, "ip =", ip)
            print ("string =", cur)
            print ("stack =", stack)
            if top in self.name_set:
                l = self.sheet[self.name_dict[top]][self.terminator_dict[ip]]
                if len(l) < 1:
                    raise WrongGrammar("error at {}, the production expression not matched.".format(ip))
                stack.pop()
                stack.extend([x for x in reversed(l) if x != Config.null])
            else:
                if (top == ip):
                    pos += 1
                    stack.pop()
                else:
                    raise WrongGrammar("error at {}, the top of stack not match with grammar settings".format(ip))

        print ("====================== {} ========================".format("Analyze Success!"))

    def analyze_string(self, string):
        print ("====================== {} =========================".format("start analyze"))
        stack = ['#', self.sheet[1][0][0]]
        cur = string.split(' ')
        cur.append('#')

        pos = 0
        i = 0
        while not (stack[-1] == '#' and cur[pos] == '#'):
            ip = cur[pos]
            top = stack[-1]
            print ("top =", top, "ip =", ip)
            print ("string =", cur)
            print ("stack =", stack)
            if top in self.name_set:
                l = self.sheet[self.name_dict[top]][self.terminator_dict[ip]]
                if len(l) < 1:
                    raise WrongGrammar("error at {}, the production expression not matched.".format(ip))
                stack.pop()
                stack.extend([x for x in reversed(l) if x != Config.null])
            else:
                if (top == ip):
                    pos += 1
                    stack.pop()
                else:
                    raise WrongGrammar("error at {}, the top of stack not match with grammar settings".format(ip))

        print ("====================== {} ========================".format("Analyze Success!"))

