from config import Config

class Lexical(object):
    """Lexical object, contains line number, start postion and end postion in a line, the tag of data and the content of data"""
    def __init__(self, line_num, start_pos, end_pos, tag, content):
        super(Lexical, self).__init__()
        self.line_num = line_num
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.tag = tag
        self.content = content

    def display(self):
         print ("line {:<4}: < {:3} : {:3} > - ( {} : {} )".format(
                self.line_num, self.start_pos, self.end_pos,
                self.tag, self.content))

class LexicalResult(object):
    """List of result, init from file"""
    def __init__(self):
        super(LexicalResult, self).__init__()

    def init_from_file(self, result_file_path, code_file_path):
        with open(code_file_path) as f:
            self.code_line_list = [line for line in f]
        self.result_list = []
        with open(result_file_path) as f:
            line_list = [line.strip() for line in [line for line in f]]
        for line in line_list:
            data = line.split(' ');
            self.result_list.append(Lexical(int(data[0]), int(data[1]), int(data[2]), data[3], data[4]))

    def display(self):
        for result in self.result_list:
            result.display()
