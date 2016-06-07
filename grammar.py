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
        self.name_set = set()

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
        new_name = reg.name + Config.suffix
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
            reg = [reg for reg in self.regs if reg.name == string][0]
            if len(reg.first) < 1:
                return self.do_first_from_reg(reg)
            else:
                return reg.first
        else:
            return set([string]);

    def get_follow_set(self):
        self.regs[0].follow.update(['#'])
        for reg in self.regs:
            self.do_follow_reg(reg)

    def do_follow_reg(self, reg):
        for content in reg.contents:
            self.do_follow_content(reg.observer, reg.name, reg.first, reg.follow, content)

    def do_follow_content(self, reg_observer, reg_name, reg_first, reg_follow, content):
        for index in range(len(content) - 1):
            # print ("index =", index)
            if content[index] in self.name_set:
                reg = [reg for reg in self.regs if reg.name == content[index]][0]
                # print ("find the reg {} in name_set of name :".format(reg.name), reg_name)
                [reg.add_to_follow(string) for string in self.do_first(content[index + 1]) if string != Config.null]
                if Config.null in self.do_first(content[index + 1]):
                    reg.follow.update(reg_follow)
                    if reg.name != reg_name:
                        reg_observer.append(reg)
                # print ("now the follow of reg {} is :".format(reg.name), reg.follow)
        if len(content) > 0 and content[-1] in self.name_set:
            reg = [reg for reg in self.regs if reg.name == content[-1]][0]
            reg.follow.update(reg_follow)
            if reg.name != reg_name:
                reg_observer.append(reg)

    def build_sheet(self):
        string_set = set()
        name_list = [reg.name for reg in self.regs]
        [[string_set.update(reg.first), string_set.update(reg.follow)] for reg in self.regs]
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


        for reg in self.regs:
            row = name_dict[reg.name] + 1
            for content in reg.contents:
                if content == []:
                    content = [Config.null]
                c_first = self.do_first_from_content(content)
                [self.sheet[row][terminator_dict[ter] + 1].extend(content) for ter in c_first if ter not in self.name_set]
                if Config.null in c_first:
                    [self.sheet[row][terminator_dict[v] + 1].extend(content) for v in reg.follow if v not in self.name_set]

