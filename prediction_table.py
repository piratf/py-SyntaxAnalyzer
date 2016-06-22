# -*- coding: utf-8 -*
# Filename: prediction_table.py

__author__ = 'Piratf'

from grammar import Grammar
from config import Config
from my_exceptions import WrongGrammar


class PredictionTable(object):
    """the to dimensional sheet to analyze grammar"""

    def __init__(self, grammar):
        super(PredictionTable, self).__init__()
        self.name_set = grammar.name_set
        self.init_sheet(grammar)
        self.errors = []
        self.tree = {}

    def display(self):
        print('========================== {} ========================='.format(
            'prediction table display'))
        for row in self.sheet:
            for part in row:
                string = '[' + ' '.join(part) + ']'
                print(string, end=' ')
                print(' '.join(['' for x in range(15 - len(string))]), end='')
            print()
        print('========================== {} ==========================\n'.format(
            'prediction table display end'))

    def init_sheet(self, grammar):
        string_set = set()
        name_list = [reg.name for reg in grammar.regs]
        [[string_set.update(reg.first), string_set.update(reg.follow)]
         for reg in grammar.regs]
        # print ("string set = ")
        # print (string_set)
        # pretreatment table
        self.sheet = [[[] for x in range(len(string_set) + 1)]
                      for x in range(len(name_list) + 1)]
        self.terminator_dict = {value: index + 1 for index,
                                value in enumerate(sorted(string_set))}
        self.name_dict = {value: index + 1 for index,
                          value in enumerate(name_list)}
        for k, v in self.terminator_dict.items():
            self.sheet[0][v].append(k)
        for k, v in self.name_dict.items():
            self.sheet[v][0].append(k)

        for reg in grammar.regs:
            row = self.name_dict[reg.name]
            for content in reg.contents:
                if content == []:
                    content = [Config.null]
                c_first = grammar.do_first_from_content(content)
                [self.sheet[row][self.terminator_dict[ter]].extend(
                    content) for ter in c_first if ter not in self.name_set]
                if Config.null in c_first:
                    [self.sheet[row][self.terminator_dict[v]].extend(
                        content) for v in reg.follow if v not in self.name_set]

    def push_error(self, ip, pos):
        self.error_cnt += 1
        self.errors.append((ip, pos))

    def deal_error(self, lexical, ip, pos):
        lr_list = lexical.result_list
        print('========================= error ========================')
        print("error at {}, the production expression not matched.".format(ip))
        line = lexical.code_line_list[lr_list[pos].line_num].strip()
        print('at line {:<3} column {:<3}:'.format(
            lr_list[pos].line_num + 1, lr_list[pos].start_pos), line)
        print('                        ' +
              ' '.join(['' for x in range(lr_list[pos].start_pos + 1)]), end='')
        print('^', end='')
        print(
            ' '.join(['' for x in range(len(line) - lr_list[pos].start_pos)]))

        print('--------------------------------------------------------')

    def analyze(self, lexical):
        self.error_cnt = 0
        print('====================== {} ========================='.format(
            "start analyze"))
        stack = ['#', self.sheet[1][0][0]]

        self.tree[self.sheet[1][0][0]] = {}
        layer = self.tree
        layer_stack = []
        layer_cnt = 0
        layer_mark = 0

        lr_list = lexical.result_list
        cur = [c.tag for c in lr_list]
        cur.append('#')

        pos = 0
        i = 0
        while not (stack[-1] == '#' and cur[pos] == '#'):
            ip = cur[pos]
            top = stack[-1]
            print ('')
            print('top =', top, 'ip =', ip)
            print('string =', cur[pos:])
            print('stack =', stack)
            if top in self.name_set:
                try:
                    l = self.sheet[self.name_dict[top]][
                        self.terminator_dict[ip]]
                except KeyError as e:
                    self.push_error(ip, pos)
                    pos += 1
                    continue

                if len(l) < 1:
                    if ip == '#':
                        print(
                            '============= no more lexicals, system logout ==============')
                        print(
                            '============= Unrecoverable error ==========================')
                        return
                    self.push_error(ip, pos)
                    pos += 1
                    continue
                stack.pop()
                pre_len = len(stack)
                print ('pre len =', pre_len)
                stack.extend([x for x in reversed(l) if x != Config.null])
                print ('cur len =', len(stack))
                if len(stack) == pre_len:
                    # print (layer)
                    # [print (x) for x in layer_stack]
                    print ('---empty')
                    layer_cnt -= 1
                    if (layer_cnt == 0):
                        layer = layer_stack[-1][0]
                        layer_stack.pop()
                        layer_cnt = 1
                        layer_mark = layer_stack[-1][1]
                    # print (layer)
                    # [print (x) for x in layer_stack]
                else:
                    print ('>>> add')
                    layer_mark += 1
                    # if len(layer_stack) > 0 and layer_stack[-1] != layer:
                    if len(layer_stack) == 0 or layer != layer_stack[-1][0]:
                        layer_stack.append((layer, layer_mark))
                    layer = layer[top]
                    layer_cnt = len(l)
                    for x in l:
                        layer[x] = {}
                    layer['layer'] = layer_mark
                    # print (layer)
                    # [print (x) for x in layer_stack]
            else:
                print ('---terminal')
                layer_cnt -= 1
                if (layer_cnt == 0):
                    layer = layer_stack[-1][0]
                    layer_stack.pop()
                    layer_cnt = 1
                    layer_mark = layer_stack[-1][1]
                # print (layer)
                # [print (x) for x in layer_stack]
                if (top == ip):
                    pos += 1
                    stack.pop()
                else:
                    self.push_error(ip, pos)
                    pos += 1
                    continue

        if self.error_cnt == 0:
            print('====================== {} ========================'.format(
                'Analyze Success!'))
        else:
            print('=========== Analyze completed, {} error{} found ==========='.format(
                self.error_cnt, '' if self.error_cnt < 2 else 's'))

        # print errors
        for x in self.errors:
            self.deal_error(lexical, x[0], x[1])
        print('==========================================================')
        self.bfs()
        # self.display_tree()
        return self.tree

    def bfs(self):
        stack = [v for k, v in self.tree.items()]
        print (stack)
        while len(stack) > 0:
            cur = stack[-1]
            print (cur)
            stack.pop()
            # print (cur[0])
            for k, v in cur.items():
                if (k != 'layer'):
                    print ('k =', k)
                    if len(v) > 0:
                        stack.append(v)

    def display_tree(self):
        print (self.tree)
        print('print tree')
        self.layers = [[]]
        self.layers[0].extend([x[0] for x in self.tree.items()])
        # [print (x[0]) for x in self.tree.items()]
        [self._display_tree(x) for x in self.tree.items()]
        print (self.layers)

    def _display_tree(self, node):
        num = node[1]['layer']
        if len(self.layers) < num + 1:
            self.layers.extend([x for x in range(num + 1 - len(self.layers))])

        self.layers[num] = []
        if node[0] != 'layer':
            # print(node[0])
            # print ([x[0] for x in node[1].items()])
            # print ('layer:', num)
            self.layers[num].extend([x[0] for x in node[1].items() if x[0] != 'layer'])
            [self._display_tree(x) for x in node[1].items() if x[0] != 'layer' and len(x[1].items()) > 0]
            # print ()

    def analyze_string(self, string):
        print("====================== {} =========================".format(
            "start analyze"))
        stack = ['#', self.sheet[1][0][0]]
        cur = string.split(' ')
        cur.append('#')

        pos = 0
        i = 0
        while not (stack[-1] == '#' and cur[pos] == '#'):
            ip = cur[pos]
            top = stack[-1]
            print("top =", top, "ip =", ip)
            print("string =", cur[pos:])
            print("stack =", stack)
            if top in self.name_set:
                l = self.sheet[self.name_dict[top]][self.terminator_dict[ip]]
                if len(l) < 1:
                    raise WrongGrammar(
                        "error at {}, the production expression not matched.".format(ip))
                stack.pop()
                stack.extend([x for x in reversed(l) if x != Config.null])
            else:
                if (top == ip):
                    pos += 1
                    stack.pop()
                else:
                    raise WrongGrammar(
                        "error at {}, the top of stack not match with grammar settings".format(ip))

        print("====================== {} ========================".format(
            "Analyze Success!"))
