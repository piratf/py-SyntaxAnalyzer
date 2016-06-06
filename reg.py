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
        self.sort_contents()
    
    def display(self):
        print ("======= {} =======".format("reg display"))
        print ("name = {}".format(self.name))
        print ("content:")
        for x in self.contents:
            print ('  -',x)
        print ("======= {} =======".format("display end"))

    # sort by start with name
    def sort_contents(self):
        self.contents.sort(key = lambda x: x.startswith(self.name), reverse = True);

    # get the last part of the string which starts wich name
    def get_str_list_after_my_head(self):
        return [x.replace(self.name, '', 1) for x in self.contents if x.startswith(self.name)]

    def get_the_str_after_this_head(self, pos, head):
        return self.contents[pos].replace(head, '', 1)

    def get_pos_list_if_startwith_prefix(self, prefix):
        return [x for x in range(0, len(self.contents)) if self.contents[x].startswith(prefix)]

    def extract_left_factor(self):
        new_reg_list = []
        for loop in range(100):
            break_flag = True
            for content in self.contents:
                temp = []
                max_cnt = 0;
                prefix = 0
                prefix_pos = 0
                for index, char in enumerate(content):
                    book = self.get_pos_list_if_startwith_prefix(content[0:index + 1])
                    if len(book) >= max_cnt:
                        temp = book
                        prefix = content[0: index + 1]
                        prefix_pos = index + 1
                        max_cnt = len(book)
                if max_cnt > 1:
                    break_flag = False
                    break;

            if break_flag:
                break;
            else:
                new_name = self.name + '`'
                new_content = []
                for x in sorted(book, reverse=True):
                    # print (self.contents)
                    # print ("del", self.contents[x])
                    if (prefix_pos >= len(self.contents[x])):
                        new_content.append(Config.null)
                    else:
                        new_content.append(self.contents[x][len(prefix):])
                    del self.contents[x]
                self.contents.append(prefix + new_name)
                new_reg_list.append(Reg(new_name, new_content))
        return new_reg_list    


