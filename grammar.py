# -*- coding: utf-8 -*
# Filename: grammar.py

__author__ = 'Piratf'

from reg import Reg, RegError

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
        contents = [x + name for x in reg.get_strlist_after_my_head()]
        old_contents = [x + name for x in reg.contents if not x.startswith(reg.name)]
        if (len(contents) > 0 and len(old_contents) > 0):
            contents.append('\e')
            self.regs.append(Reg(name, contents))
            reg.contents = old_contents
        elif (len(contents) > 0 and len(old_contents) <= 0):
            raise RegError("this reg can't be processed. - {}".format(reg));

    # remove Indirect left recursion from grammar
    def remove_indirect_left_recursion(self):
        for i in range(1, len(self.regs) + 1):
            for j in range(0, i):
                if (i < len(self.regs)):
                    ai = self.regs[i]
                    aj = self.regs[j]
                    deal = ai.find(aj)
                    for x in ai.find(aj):
                        [ai.contents.append(jcontent + ai.get_the_str_after_this_head[x, aj.name]) for jcontent in aj.contents]
                        del ai[x]
                    self.remove_direct_left_recursion(i)
                else:
                    self.remove_direct_left_recursion(j)
                
