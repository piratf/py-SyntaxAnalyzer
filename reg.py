# -*- coding: utf-8 -*
# Filename: reg.py

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

