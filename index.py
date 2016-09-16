import sys, pygame
from pygame.locals import *

from pprint import pprint

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((1024, 768), 0, 0)
pygame.display.set_caption('EasyBox')

def dict_merge(d1, d2):
    return dict(list(d1.items()) + list(d2.items()))

style_defaults = {
  'x': 'auto',
  'y': 'auto',
  'w': 'auto',
  'h': 'auto',
  'padding': '0',
  'background_color': 'transparent'
}

# 'position': 'relative',
# 'color': 'inherits',
# 'backgroundImage': 'none',
# 'backgroundPosition': '0, 0',
# 'backgroundOrigin': 'padding-box',
# 'fontFamily': 'OpenSans-Regular',
# 'fontSize': '16',
# 'padding': '0',
# 'borderWidth': '0',
# 'borderColor': '000, 000, 000'

'''
class Box(object):

    def __init__(self, style={}):
        self.parent = None
        self.__children = []
        self.__style = {}
        self.__style_computed = {}

    @property
    def style(self):
        return self.__style

    @style.setter
    def style(self, style_changed):
        self.__style = dict_merge(self.__style, style_changed)
        self.__update_style_computed(style_changed)

    def __update_style_computed(self, style_changed):
        for key, value in style_changed.items():
            self.__style_computed[key] = getattr(self, '_Box__compute_%s' % key)()

        if (key in style_changed.keys() for key in ('x', 'padding')):
            self.__style_computed['x_computed'] = self.__compute_x_content()

    @property
    def style_computed(self):
        return self.__style_computed

    # see: http://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    def props(self, *props, **kwargs):
        for d in props:
            for key in d:
                setattr(self, key, d[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def add(self, box):
        box.parent = self
        self.__children.append(box)
        box.style = dict_merge(style_defaults, box.style)

    def __compute_x(self):
        style_value = self.__style['x']
        return self.parent.style_computed['x_computed'] if style_value == 'auto' else int(style_value)

    def __compute_x_content(self):
        return self.style_computed['x'] + self.style_computed['padding']

    def __compute_y(self):
        style_value = self.__style['y']
        return self.parent.style_computed['y'] if style_value == 'auto' else int(style_value)

    def __compute_w(self):
        style_value = self.__style['w']
        return self.parent.style_computed['w'] if style_value == 'auto' else int(style_value)

    def __compute_h(self):
        style_value = self.__style['h']
        return self.parent.style_computed['h'] if style_value == 'auto' else int(style_value)

    def __compute_padding(self):
        style_value = self.__style['padding']
        return int(style_value)

    def __compute_background_color(self):
        style_value = self.__style['background_color']
        return self.parent.style_computed['background_color'] if style_value == 'transparent' else style_value
'''

class Box(object):

    def __init__(self):
        self.parent = None
        self.children = []

        self.x = 'auto'
        self.y = 'auto'
        self.w = 'auto'
        self.h = 'auto'
        self.background_color = 'transparent'
        self.padding_top = 0
        self.padding_right = 0
        self.padding_bottom = 0
        self.padding_left = 0
        self.color = 'inherits'

    def add(self, box):
        box.parent = self
        self.children.append(box)

    def compute_x(self):
        if self.x == 'auto':
            return self.parent.compute_content_x()
        else:
            return self.parent.compute_content_x() + self.x

    def compute_content_x(self):
        return self.compute_x() + self.padding_left

    def compute_y(self):
        if self.y == 'auto':
            return self.parent.compute_content_y()
        else:
            return self.parent.compute_content_y() + self.y

    def compute_content_y(self):
        return self.compute_y() + self.padding_top

    def compute_w(self):
        return self.parent.compute_content_w() if self.w == 'auto' else self.w

    def compute_content_w(self):
        return self.compute_w() - self.padding_left - self.padding_right

    def compute_h(self):
        return self.parent.compute_content_h() if self.h == 'auto' else self.h

    def compute_content_h(self):
        return self.compute_h() - self.padding_top - self.padding_bottom

    def compute_background_color(self):
        return self.parent.compute_background_color() if self.background_color == 'transparent' else self.background_color

class BoxRenderer(object):

    def __init__(self):
        pass

    def render(self, box):
        box_rect = pygame.Rect(
          (box.compute_x(), box.compute_y()),
          (box.compute_w(), box.compute_h()),
        )
        pygame.draw.rect(
          windowSurface,
          box.compute_background_color(),
          box_rect
        )

class EasyBox(object):

    def __init__(self, screen):
       self.box_root = self.create_root(screen)

    def create_root(self, screen):
        screen_rect = screen.get_rect()

        box = Box()
        box.x = screen_rect.x
        box.y = screen_rect.y
        box.w = screen_rect.w
        box.h = screen_rect.h
        box.background_color = (000, 000, 000)
        # override box methods
        box.compute_content_x = lambda: screen_rect.x
        box.compute_content_y = lambda: screen_rect.y
        box.compute_content_w = lambda: screen_rect.w
        box.compute_content_h = lambda: screen_rect.h
        return box

    def create_box(self):
        box = Box()
        self.box_root.add(box)
        return box


if __name__ == '__main__':

    container = EasyBox(screen=windowSurface)

    box1 = container.create_box()
    box1.x = 10
    box1.y = 20
    box1.w = 800
    box1.h = 600
    box1.padding_left = 20
    box1.padding_right = 20
    box1.background_color = (150, 000, 000)

    box2 = container.create_box()
    box2.x = 50
    box2.y = 10
    box2.w = 400
    box2.h = 300
    box2.background_color = (000, 150, 000)

    box1.add(box2)

    renderer = BoxRenderer()
    renderer.render(box1)
    renderer.render(box2)

    pygame.display.update()

    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
