import tkinter
from tkinter import ttk
from tkinter_gl import GLViewBase
from OpenGL import GL

import time

class GLView(GLViewBase):
    def __init__(self, parent):
        super().__init__(parent)

        self.size = 0.5
        self.x = 0.0
        self.y = 0.0

    def draw(self):
        self.make_current()
 
        GL.glViewport(0, 0, self.winfo_width(), self.winfo_height())

        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2d( self.x + self.size,  self.y + self.size)
        GL.glVertex2d( self.x + self.size,  self.y - self.size)
        GL.glVertex2d( self.x - self.size,  self.y - self.size)
        GL.glVertex2d( self.x - self.size,  self.y + self.size)
        GL.glEnd()

        while True:
            err = GL.glGetError()
            if err == GL.GL_NO_ERROR:
                break
            print("Error: ", err)

        self.swap_buffers()

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.key_pressed = None
        self.time_pressed = 0

        self.label = ttk.Label(self, text="Use cursor keys to move square")
        self.label.grid(row=0, column=0)

        self.gl_view = GLView(self)
        self.gl_view.grid(row=1, column=0)

        self.bind('<KeyPress>', self.handle_key_press)
        self.bind('<KeyRelease>', self.handle_key_release)

    def set_size(self, value):
        self.gl_view.size = float(value)
        self.gl_view.draw()

    def handle_key_press(self, event):
        self.key_pressed = event.keysym.lower()
        self.time_pressed = time.time()

        if self.key_pressed in ['left', 'right', 'up', 'down']:
            self.after(5, self.advance)

    def handle_key_release(self, event):
        self.key_pressed = None

    def advance(self):
        if self.key_pressed is None:
            return

        self.gl_view.draw()
        t = time.time()

        delta = 0.1 * (t - self.time_pressed)

        if self.key_pressed == 'left':
            self.gl_view.x -= delta
        if self.key_pressed == 'right':
            self.gl_view.x += delta
        if self.key_pressed == 'up':
            self.gl_view.y += delta
        if self.key_pressed == 'down':
            self.gl_view.y -= delta

        self.time_pressed = t
        self.after(5, self.advance)

if __name__ == '__main__':

    window = Window()

    sliderWindow = tkinter.Tk()
    slider = ttk.Scale(master=sliderWindow,
                       orient=tkinter.HORIZONTAL,
                       command=window.set_size,
                       value=window.gl_view.size)
    slider.grid(row=0, column=0, sticky=tkinter.NSEW)

    print("Using OpenGL", window.square_widget.gl_version())

    window.mainloop()

