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

    def __eq__(self, other):
        return self.regs == other.regs

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
                    ai.sort_contents()
                    self.remove_direct_left_recursion(i)
                else:
                    self.remove_direct_left_recursion(j)
        [self.regs.insert(index, reg) for index, reg in sorted(self.temp.items(), reverse=True)]
        self.temp.clear()

    def extract_left_factor(self):
        new_reg_list = []
        for index, reg in enumerate(self.regs):
            [new_reg_list.append([index + 1, x]) for x in reg.extract_left_factor()]
        [self.regs.insert(pos, x) for pos, x in new_reg_list]
                
    def get_first_set(self):
        self.name_set = set([reg.name for reg in self.regs])
        for reg in reversed(self.regs):
            reg.first.update(self.do_first_from_reg(reg))

    # todo: the string or change to list
    def do_first_from_reg(self, reg):
        return self.do_first_from_list(reg.contents)

    def do_first_from_list(self, contents):
        first = set()
        for content in contents:
            # print ("first =", first)
            # print ("content =", content)
            first.update(self.do_first_from_content(content))
        return first

    def do_first_from_content(self, content):
        if len(content) < 1:
            return set([Config.null])
        first_content = set()
        left = Config.null
        for string in content:
            right = string
            if Config.null in self.do_first(left):
                first_content.update(self.do_first(right))
                # print ("first content =", first_content)
            else:
                return first_content
            left = right
        right = Config.null
        if Config.null in self.do_first(left):
            first_content.update(self.do_first(right))
        return first_content

    def do_first(self, string):
        if (string == Config.null):
            return set([Config.null])
        elif string in self.name_set:
            return self.do_first_from_reg([reg for reg in self.regs if reg.name == string][0])
        else:
            return set([string]);



