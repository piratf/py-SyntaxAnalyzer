# -*- coding: utf-8 -*
# Filename: config.py

__author__ = 'Piratf'

class Config(object):
    """config for parser"""
    @classmethod
    def __init__(self):
        super(Config, self).__init__()
    
    @classmethod
    def read_config(self):
        with open('config.conf') as conf:
            line = conf.readline()
            self.separator_str = self.get_config_value(line)
            line = conf.readline()
            self.split_str = self.get_config_value(line)
            line = conf.readline()
            self.null = self.get_config_value(line)
            self.suffix = '+'
            # print (self.null)
            # print (self.split_str)
            # print (self.separator_str)

    @classmethod
    def get_config_value(self, line):
        return line.split('=', 1)[1].strip()

    @classmethod
    def get_sep(self):
        return self.separator_str