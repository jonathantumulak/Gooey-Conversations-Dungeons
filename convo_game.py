from collections import OrderedDict
import pyglet
from pyglet.text import Label

from pyglet.window import key as keys

from suspect import generateSuspects

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

suspects = generateSuspects()

guilty = None
for s in suspects:
    if s.guilty is True:
        guilty = s
print guilty

active_suspect = 0

lamp_pos = [80, 485, 885]

chair = pyglet.image.load('images/prisoner_chair.png')
p1 = pyglet.image.load('images/prisoner_1.png')
p2 = pyglet.image.load('images/prisoner_2.png')
p3 = pyglet.image.load('images/prisoner_3.png')
lamp = pyglet.image.load('images/lamp_top.png')
win = pyglet.image.load('images/you_win.png')
lose = pyglet.image.load('images/you_lose.png')

intro = pyglet.image.load('images/you_lose.png')


state = 'INTRO' # INTRO, QUESTION, ANSWER, GUESS, WIN, LOSE
scene = OrderedDict()


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
        self.label = Label(at, x=300, y=150, color=QCOLOR)

    def draw(self):
        self.label.draw()

class SuspectInfo(object):
    def __init__(self, suspect):
        self.suspect = suspect
        self.x = 800
        self.y = 300
        self.labels = []
        self._build_labels()

    def _build_labels(self):
        y = 70
        x = 600
        self.labels.append(Label('age: {}'.format(self.suspect.age), x=x, y=y, color=QCOLOR))
        y+= 20
        self.labels.append(Label('height: {}'.format(self.suspect.height), x=x, y=y, color=QCOLOR))
        y+= 20
        self.labels.append(Label('job: {}'.format(self.suspect.job), x=x, y=y, color=QCOLOR))
        y+= 20
        self.labels.append(Label('nationality: {}'.format(self.suspect.nationality), x=x, y=y, color=QCOLOR))

    def draw(self):
        for label in self.labels:
            label.draw()


@window.event
def on_draw():
    window.clear()
    for k, v in scene.items():
        v.draw()


@window.event
def on_key_press(symbol, modifiers):
    global state
    global active_suspect
    global suspects

    if symbol == keys.UP:
        if state in ['QUESTION', 'GUESS']:
            scene['dialog'].select_up()

    if symbol == keys.DOWN:
        if state in ['QUESTION', 'GUESS']:
            scene['dialog'].select_down()

    if symbol == keys.ENTER:
        if state == 'INTRO':
            del scene['intro']
            state = 'QUESTION'
            scene['dialog'] = ConversationDialog('Ask a question', QUESTIONS, (20, 150))
            scene['suspect_info'] = SuspectInfo(guilty)
            scene['chair_0'] = pyglet.sprite.Sprite(chair, x=100, y=200)
            scene['chair_0'].scale = 0.5

            scene['chair_1'] = pyglet.sprite.Sprite(chair, x=500, y=200)
            scene['chair_1'].scale = 0.5

            scene['chair_2'] = pyglet.sprite.Sprite(chair, x=900, y=200)
            scene['chair_2'].scale = 0.5

            scene['p1'] = pyglet.sprite.Sprite(p1, x=125, y=335)
            scene['p1'].scale = 0.5

            scene['p2'] = pyglet.sprite.Sprite(p2, x=525, y=335)
            scene['p2'].scale = 0.5

            scene['p3'] = pyglet.sprite.Sprite(p3, x=925, y=335)
            scene['p3'].scale = 0.5

            scene['lamp'] = pyglet.sprite.Sprite(lamp, x=80, y=240)
            scene['lamp'].scale = 1
            return
        elif state == 'QUESTION':
            q = scene['dialog'].activate()
            del scene['dialog']
            if q == 'What is your age?':
                scene['adialog'] = AnswerDialog(str(suspects[active_suspect].age))
            if q == 'What is your nationality?':
                scene['adialog'] = AnswerDialog(str(suspects[active_suspect].nationality))
            if q == 'What is your height?':
                scene['adialog'] = AnswerDialog(str(suspects[active_suspect].height))
            if q == 'What is your job?':
                scene['adialog'] = AnswerDialog(str(suspects[active_suspect].job))
            state = 'ANSWER'
        elif state == 'ANSWER':
            del scene['adialog']
            state = 'GUESS'
            scene['dialog'] = ConversationDialog('Do you think I did it?', ['Pass', 'Yes'], (20, 150))
        elif state == 'GUESS':
            q = scene['dialog'].activate()
            if q == 'Yes':
                if suspects[active_suspect] == guilty:
                    state = 'WIN'
                    print 'You win!!!'
                    scene['win'] = pyglet.sprite.Sprite(win, x=300, y=100)
                    return
                else:
                    state = 'LOSE'
                    print 'You lose!!'
                    scene['lose'] = pyglet.sprite.Sprite(lose, x=200, y=140)
                    return
            if q == 'Pass':
                pass
            state = 'QUESTION'
            scene['dialog'] = ConversationDialog('Ask a question', QUESTIONS, (20, 150))
            if active_suspect == 2:
                active_suspect = 0
            else:
                active_suspect += 1
            scene['lamp'].x = lamp_pos[active_suspect]
        if state in ['WIN', 'LOSE']:
            pyglet.app.exit()

    #print '{} key was pressed'.format(symbol)

scene['intro'] = pyglet.sprite.Sprite(win, x=300, y=100)


pyglet.app.run()
