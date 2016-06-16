import pyglet
from pyglet.text import Label

from pyglet.window import key as keys


window = pyglet.window.Window(width=1280, height=720)
WW, WH = window.width, window.height

scene = {}


class ConversationDialog(object):
    def __init__(self, question, choices, pos):
        self.question = question
        self.choices = choices
        self.pos = pos
        self.labels = []
        self._build_labels()

    def _build_labels(self):
        x, y = 0, 0
        ql = Label(self.question, x=self.pos[0]+x, y=self.pos[1]+y)
        self.labels.append(ql)
        y -= 20
        for label in self.choices:
            cl = Label(label, x=self.pos[0]+x, y=self.pos[1]+y)
            self.labels.append(cl)
            y -= 20

    def draw(self):
        for label in self.labels:
            label.draw()


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
    print '{} key was pressed'.format(symbol)

scene['dialog'] = ConversationDialog('Choose your action', ['one', 'two'], (20, 200))

pyglet.app.run()
