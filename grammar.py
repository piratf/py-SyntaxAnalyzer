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
        self.temp = {}

    def add(self, reg):
        self.regs.append(reg)

    def display(self):
        print ("======= {} ===========".format("Grammar display"))
        print ("count: {}".format(len(self.regs)))

        for reg in self.regs:
            reg.display()

        print ("======= {} =======\n".format("Grammar display end"))

    # remove direct left recursion from grammar
    def remove_direct_left_recursion(self, pos):
        reg = self.regs[pos]
        new_name = reg.name + '`'
        new_contents = [x for x in reg.get_str_list_after_my_head()]
        [x.append(new_name) for x in new_contents]
        old_contents = [x[:] for x in reg.contents if len(x) > 0 and x[0] != reg.name]
        [x.append(new_name) for x in old_contents]

        if (len(new_contents) > 0 and len(old_contents) > 0):
            print ("modify in direct ")
            # todo
            new_contents.append([])
            reg = Reg(new_name, new_contents)
            self.temp[pos + 1] = reg
            self.regs[pos].contents = old_contents
        elif (len(new_contents) > 0 and len(old_contents) <= 0):
            raise RegError("this reg can't be processed. - {}".format(reg));

    # remove Indirect left recursion from grammar
    def remove_indirect_left_recursion(self):
        for i in range(1, len(self.regs) + 1):
            for j in range(0, i):
                if (i < len(self.regs)):
                    ai = self.regs[i]
                    aj = self.regs[j]
                    for x in ai.get_pos_list_if_startwith_prefix(aj.name):
                        tail = ai.get_the_str_after_its_head(x)
                        if (len(tail) > 0):
                            for jcontent in aj.contents:
                                jc = jcontent[:]
                                jc.extend(tail)
                                ai.contents.append(jc)
                            del ai.contents[x]
                    print ("before direct")
                    ai.sort_contents()
                    ai.display()
                    self.remove_direct_left_recursion(i)
                    print ("after direct")
                    ai.display()
                else:
                    self.remove_direct_left_recursion(j)
        [self.regs.insert(index, reg) for index, reg in sorted(self.temp.items(), reverse=True)]

    def extract_left_factor(self):
        new_reg_list = []
        for reg in self.regs:
            [new_reg_list.append(x) for x in reg.extract_left_factor()]
        [self.regs.append(x) for x in new_reg_list]
                
    def get_first_set(self):
        name_set = set([reg.name for reg in self.regs])
        for reg in sorted(self.regs, key=lambda x: x.name, reverse=True):
            reg.first = first(reg.name, name_set)

    # todo: the string or change to list
    def first(self, string, name_set):
        if (string in name_set):
            pass

