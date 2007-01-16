#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

from code import InteractiveConsole
import sys

from pyglet.GL.VERSION_1_1 import *
from pyglet.layout import *
from pyglet.window import *
from pyglet.window.event import *
from pyglet.window.key import *
from pyglet.clock import *

from pyglet.text import *
from pyglet.layout import *

data = '''<?xml version="1.0"?>
<html>
  <head>
    <style>
      #interpreter-block {
          white-space: pre;
          font-family: monospace;
          border-left: 5px solid silver;
          border-right: 5px solid silver;
      }
      #interpreter-block #cursor {
          white-space: pre;
      }
      #interpreter {
          white-space: pre;
      }
    </style>
  </head>
  <body>
    <h1>Interpreter example</h1>
    <div id="interpreter-block"><span
id="interpreter">&gt;&gt;&gt; </span><span id="cursor"> </span></div>
  </body>
</html>
'''

class DOMInterpreter(InteractiveConsole):
    class Stream(object):
        def __init__(self, interpreter):
            self.interpreter = interpreter
        
        def write(self, data):
            self.interpreter.write(data)

    def __init__(self, element):
        InteractiveConsole.__init__(self)
        self.element = element
        self.buffer = ''
        self.stream = DOMInterpreter.Stream(self)

        self.write('pyglet interpreter\n')
        self.write('>>> ')

    def write(self, data):
        self.element.add_text(data)

    def input(self, input):
        _stdout = sys.stdout
        sys.stdout = self.stream

        self.write(input)
        self.buffer += input
        if '\n' in self.buffer:
            source, self.buffer = self.buffer.rsplit('\n', 1)
            prompt = self.runsource(source)
            if prompt:
                self.write('\n... ')
            else:
                self.write('\n>>> ')

        sys.stdout = _stdout

    def backspace(self):
        self.buffer = self.buffer[:-1]
        # There is no easy way to change element text yet...
        self.element.text = self.element.text[:-1]
        self.element.document.element_modified(self.element)

window = Window(visible=False, vsync=False)

layout = Layout()
layout.set_xhtml(data)
window.push_handlers(layout)

interp = DOMInterpreter(layout.document.get_element('interpreter'))

def on_text(text):
    interp.input(text.replace('\r', '\n'))
window.push_handlers(on_text)

def on_key_press(symbol, modifiers):
    if symbol == K_BACKSPACE:
        interp.backspace()
    else:
        return True
window.push_handlers(on_key_press)

def blink_cursor(dt):
    cursor = layout.document.get_element('cursor')
    if cursor.style['background-color']:
        del cursor.style['background-color']
    else:
        cursor.style['background-color'] = 'black'
clock = Clock()
clock.schedule_interval(blink_cursor, 0.5)

glClearColor(1, 1, 1, 1)
window.set_visible()

while not window.has_exit:
    window.dispatch_events()
    clock.tick()
    glClear(GL_COLOR_BUFFER_BIT)
    layout.draw()

    window.flip()
