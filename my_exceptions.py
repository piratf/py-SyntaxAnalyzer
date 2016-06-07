# -*- coding: utf-8 -*
# Filename: my_exceptions.py

__author__ = 'Piratf'

class WrongGrammar(Exception):
    """Exception for wrong grammar"""
    def __init__(self, message):
        super(WrongGrammar, self).__init__()
        self.message = message
        
    def __str__(self):
        return "grammar error** : " + self.message
