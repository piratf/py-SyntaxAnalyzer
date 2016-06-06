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
        self.temp = []

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
        # name of new reg which has `
        name = reg.name + '`'
        # contents of new reg
        contents = [x.append(name) for x in reg.get_str_list_after_my_head()]
        old_contents = [x.append(name) for x in [x for x in reg.contents if not x[0] == reg.name]]
        
        if (len(contents) > 0 and len(old_contents) > 0):
            contents.append(Config.null)
            self.temp.append(pos + 1, Reg(name, contents))
            reg.contents = old_contents
        elif (len(contents) > 0 and len(old_contents) <= 0):
            raise RegError("this reg can't be processed. - {}".format(reg));

    # remove Indirect left recursion from grammar
    def remove_indirect_left_recursion(self):
        for i in range(0, len(self.regs)):
            for j in range(i + 1, len(self.regs)):
                print (i, j)
                # if j not out of range
                if (j < len(self.regs)):
                    # get ai and aj
                    ai = self.regs[i]
                    aj = self.regs[j]

                    # get each postion which start with aj's name
                    for x in ai.get_pos_list_if_startwith_prefix(aj.name):
                        # replace them through each content from aj
                        for jcontent in aj.contents:
                            temp = jcontent
                            tail = ai.get_the_str_after_this_head(x, aj.name)
                            if (len(tail) < 1):
                                continue
                            else:
                                temp.extend(tail)
                                ai.contents.append(temp)
                                del ai.contents[x]
                    self.remove_direct_left_recursion(i)
                else:
                    pass
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
            pass

