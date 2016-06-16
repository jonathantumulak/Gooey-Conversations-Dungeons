import pyglet
from pyglet.text import Label

from pyglet.window import key as keys


window = pyglet.window.Window(width=1280, height=720)
WW, WH = window.width, window.height
QCOLOR = (255, 255, 0, 255)
CCOLOR = (50, 50, 100, 255)
SCOLOR = (100, 100, 255, 255)
scene = {}



class ConversationDialog(object):
    def __init__(self, question, choices, pos):
        self.question = question
        self.choices = choices
        self.pos = pos
        self.labels = []
        self.active = 0
        self._build_labels()

    def _build_labels(self):
        self.labels = []
        x, y = 0, 0
        ql = Label(self.question, x=self.pos[0]+x, y=self.pos[1]+y, color=QCOLOR)
        self.labels.append(ql)
        y -= 20
        n = 0
        for label in self.choices:
            if n == self.active:
                color = SCOLOR
            else:
                color = CCOLOR
            cl = Label(label, x=self.pos[0]+x, y=self.pos[1]+y, color=color)
            self.labels.append(cl)
            y -= 20
            n += 1

    def draw(self):
        for label in self.labels:
            label.draw()

    def select_up(self):
        if self.active == 0:
            return
        self.active -= 1
        self._build_labels()

    def select_down(self):
        if self.active == len(self.choices)-1:
            return
        self.active += 1
        self._build_labels()

    def activate(self):
        return self.choices[self.active]


# scene['hello_label'] = pyglet.text.Label('Hello, world',
#                           #font_name='Times New Roman',
#                           font_size=36,
#                           x=window.width//2, y=window.height//2,
#                           anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    for k, v in scene.items():
        v.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == keys.ESCAPE:
        print 'Pressed ESC'
        return True
    if symbol == keys.UP:
        print 'UP'
        scene['dialog'].select_up()
    if symbol == keys.DOWN:
        print 'DOWN'
        scene['dialog'].select_down()
    if symbol == keys.ENTER:
        print 'Activation Returned:', scene['dialog'].activate()
    print '{} key was pressed'.format(symbol)

scene['dialog'] = ConversationDialog('Choose your action', ['one', 'two'], (20, 200))

pyglet.app.run()
