# -*- coding: utf-8 -*
# Filename: grammar.py

__author__ = 'Piratf'

from reg import Reg, RegError
from config import Config

class Grammar(object):
    """list of regs"""
    def __init__(self, regs):
        super(Grammar, self).__init__()
        self.regs = regs
    
    def add(self, reg):
        self.regs.append(reg)

    def display(self):
        print ("======= {} ===========".format("Grammar display"))
        print ("count: {}".format(len(self.regs)))

        for reg in self.regs:
            reg.display()

        print ("======= {} =======".format("Grammar display end"))

    # remove direct left recursion from grammar
    def remove_direct_left_recursion(self, pos):
        reg = self.regs[pos]
        # name of new reg which has `
        name = reg.name + '`'
        # contents of new reg
        contents = [x + name for x in reg.get_str_list_after_my_head()]
        old_contents = [x + name for x in reg.contents if not x.startswith(reg.name)]
        if (len(contents) > 0 and len(old_contents) > 0):
            contents.append(Config.null)
            self.regs.insert(pos + 1, Reg(name, contents))
            reg.contents = old_contents
        elif (len(contents) > 0 and len(old_contents) <= 0):
            raise RegError("this reg can't be processed. - {}".format(reg));

    # remove Indirect left recursion from grammar
    def remove_indirect_left_recursion(self):
        for i in range(1, len(self.regs) + 1):
            for j in range(0, i):
                # if i not out of range
                if (i < len(self.regs)):
                    # get ai and aj
                    ai = self.regs[i]
                    aj = self.regs[j]
                    
                    # get each postion which start with aj's name
                    for x in ai.get_pos_list_if_startwith_prefix(aj.name):
                        # replace them through each content from aj
                        [ai.contents.append(jcontent + ai.get_the_str_after_this_head[x, aj.name]) for jcontent in aj.contents]
                        del ai[x]
                    self.remove_direct_left_recursion(i)
                else:
                    self.remove_direct_left_recursion(j)

    def extract_left_factor(self):
        new_reg_list = []
        for reg in self.regs:
            [new_reg_list.append(x) for x in reg.extract_left_factor()]
        [self.regs.append(x) for x in new_reg_list]
                
    def get_first_set(self):
        name_set = set([reg.name for reg in self.regs])
        print (name_set)
        for reg in sorted(self.regs, key=lambda x: x.name, reverse=True):
            reg.first = first(reg.name, name_set)

    # todo: the string or change to list
    def first(self, string, name_set):
        if (string in name_set):
                 

