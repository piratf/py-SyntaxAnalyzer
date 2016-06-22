from PIL import Image, ImageDraw, ImageFont
import PIL

fontsize = 27
font = ImageFont.truetype("UbuntuMono-B.ttf", fontsize)

class Paint(object):
    """paint tree"""
    def __init__(self):
        super(Paint, self).__init__()
        self.arr = ['E', '12333', ';']
        self.vertical = 150
        self.horizontal = 10
        self.width = 120
        self.height = 70
        self.left = self.vertical
        self.right = self.left;
        self.gap_width = 30

    def save(self, filePath):
        self.im.save(filePath, "PNG")

    def draw_node(self, left, top, right, bottom, font, content):
        center = (left + self.width / 2, top + self.height / 2)
        font_size = font.getsize(content)
        print (fontsize)
        font_pos = (0, 0)
        font_pos = (center[0] - font_size[0] / 2, center[1] - font_size[1] / 2 - 5)
        print (font_pos)
        print (left)
        self.draw.arc((left, top, right, bottom), 0, 360, fill=(0, 0, 0))
        self.draw.text(font_pos, content, fill=(50, 50, 50), font=font)

    def draw_list(self, arr, left, top):
        right = left
        for k, v in enumerate(arr):
            print (k, v)
            top = self.horizontal
            bottom = top + self.height
            right = left + self.width
            print (font.getsize(v))
            self.draw_node(left, top, right, bottom, font, v)
            left = right + self.gap_width

    def draw_tree(self, tree):
        self.process(tree)
        self.im = Image.new('RGB', (1024, 1024), 'white')
        self.draw = ImageDraw.Draw(self.im)
        self.draw_list(tree.keys(), 10, 500)
        self.im.save('x.png', "PNG")

    def process(self, tree):
        self.layers = []


