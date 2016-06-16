import pyglet
from pyglet.window import key as keys


window = pyglet.window.Window(width=1280, height=720)

scene = {}


scene['hello_label'] = pyglet.text.Label('Hello, world',
                          #font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')


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


pyglet.app.run()
