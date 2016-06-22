# -*- coding: utf-8 -*
# Filename: reg.py

from config import Config

__author__ = 'Piratf'

class RegError(Exception):
    """exception class for Reg"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Reg(object):
    """regex string: name and content"""
    def __init__(self, name, contents):
        super(Reg, self).__init__()
        self.name = str(name)
        self.contents = contents
        self.first = set()
        self.follow = set()
        self.observer = []
        self.sort_contents()

    def __eq__(self, other):
        return self.name == other.name and sorted(self.contents) == sorted(other.contents)

    def display(self):
        print ("======= {} =======".format("reg display"))
        print ("name = {}".format(self.name))
        print ("content:")
        for x in self.contents:
            if (len(x) == 0):
                print ('  -', ['\e'])
            else:
                print ('  -',x)

        print ("first set:")
        print (self.first)
        print ("follow set:")
        print (self.follow)

        print ("======= {} =======".format("display end"))

    # sort by start with name
    def sort_contents(self):
        self.contents.sort(key = lambda x: len(x) > 0 and x[0] == self.name, reverse = True);

    # get the last part of the string which starts wich name
    def get_str_list_after_my_head(self):
        return [x[1:] for x in self.contents if len(x) > 1 and x[0] == self.name]

    def get_the_str_after_its_head(self, pos):
        if (len(self.contents[pos]) <= 1):
            return []
        return self.contents[pos][1:]

    def get_pos_list_if_startwith_prefix(self, prefix):
        print ("contents =", self.contents)
        print ("prefix =", prefix)
        for index, content in enumerate(self.contents):
            if len(content) > len(prefix) and content[0:len(prefix)] == prefix:
                print (content[0:len(prefix)])
        return [index for index, content in enumerate(self.contents) if len(content) >= len(prefix) and content[0:len(prefix)] == prefix]

    def extract_left_factor(self):
        new_reg_list = []
        while True:
            break_flag = True
            for content in self.contents:
                book = []
                max_cnt = 0;
                prefix = []
                prefix_pos = 0
                for index, string in enumerate(content):
                    temp = self.get_pos_list_if_startwith_prefix(content[ :index + 1])
                    if len(temp) >= max_cnt:
                        book = temp
                        prefix = content[0: index + 1]
                        prefix_pos = index + 1
                        max_cnt = len(temp)
                if max_cnt > 1:
                    break_flag = False
                    break;

            if break_flag:
                break;
            else:
                new_name = self.name + Config.suffix
                new_content = []
                for x in sorted(book, reverse=True):
                    # print ("prefix =", prefix)
                    # print ("del", self.contents[x])
                    if (prefix_pos >= len(self.contents[x])):
                        new_content.append([])
                    else:
                        new_content.append(self.contents[x][prefix_pos:])
                    del self.contents[x]
                prefix.append(new_name)
                self.contents.append(prefix)
                new_reg_list.append(Reg(new_name, new_content))
        return new_reg_list

    def add_to_follow(self, string):
        self.follow.add(string)
        for o in self.observer:
            o.add_to_follow(string)

    def update_follow(self, other_follow):
        self.follow.update(other_follow)
        for o in self.observer:
            o.update_follow(other_follow)
