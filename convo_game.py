import pyglet
from pyglet.text import Label

from pyglet.window import key as keys


window = pyglet.window.Window(width=1280, height=720)
WW, WH = window.width, window.height
QCOLOR = (255, 255, 0, 255)
CCOLOR = (50, 50, 100, 255)
SCOLOR = (100, 100, 255, 255)
ACOLOR = (255, 255, 255, 255)

QUESTIONS = [
    'What is your age?',
    'What is your nationality?',
    'What is your height?',
    'What is your job?'
]

state = 'QUESTION' # QUESTION, ANSWER, GUESS
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

class AnswerDialog(object):
    def __init__(self, answer_text):
        at = 'The goo says, "{}"'.format(answer_text)
        self.label = Label(at, x=300, y=300, color=QCOLOR)

    def draw(self):
        self.label.draw()


@window.event
def on_draw():
    window.clear()
    for k, v in scene.items():
        v.draw()


@window.event
def on_key_press(symbol, modifiers):
    global state
    if symbol == keys.UP:
        if state in ['QUESTION', 'GUESS']:
            scene['dialog'].select_up()

    if symbol == keys.DOWN:
        if state in ['QUESTION', 'GUESS']:
            scene['dialog'].select_down()

    if symbol == keys.ENTER:
        if state == 'QUESTION':
            q = scene['dialog'].activate()
            del scene['dialog']
            if q == 'What is your age?':
                scene['adialog'] = AnswerDialog('22')
            if q == 'What is your nationality?':
                scene['adialog'] = AnswerDialog('American')
            if q == 'What is your height?':
                scene['adialog'] = AnswerDialog('2.5 goos')
            if q == 'What is your job?':
                scene['adialog'] = AnswerDialog('Security Guard')
            state = 'ANSWER'
        elif state == 'ANSWER':
            del scene['adialog']
            state = 'GUESS'
            scene['dialog'] = ConversationDialog('Do you think I did it?', ['Yes', 'Pass'], (20, 200))
        elif state == 'GUESS':
            q = scene['dialog'].activate()
            if q == 'Yes':
                pass
            if q == 'Pass':
                pass
            state = 'QUESTION'
            scene['dialog'] = ConversationDialog('Ask a question', QUESTIONS, (20, 200))

    #print '{} key was pressed'.format(symbol)

scene['dialog'] = ConversationDialog('Ask a question', QUESTIONS, (20, 200))


pyglet.app.run()
