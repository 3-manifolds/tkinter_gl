import tkinter
from tkinter import ttk
from tkinter_gl import GLViewBase
from OpenGL import GL

import time

separate_slider = True

class GLView(GLViewBase):
    def __init__(self, parent):
        super().__init__(parent)

        self.size = 0.5
        self.x = 0.0
        self.y = 0.0

    def set_size(self, value):
        self.size = float(value)
        self.draw()

    def draw(self, event=None):
 
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

        self.glView = GLView(self)
        self.glView.grid(row=1, column=0)

        if not separate_slider:
            self.slider = ttk.Scale(master=self,
                                    orient=tkinter.HORIZONTAL,
                                    command=self.glView.set_size,
                                    value=self.glView.size)
            self.slider.grid(row=1, column=0, sticky=tkinter.NSEW)

        self.bind('<KeyPress>', self.tkKeyPress)
        self.bind('<KeyRelease>', self.tkKeyRelease)

    def tkKeyPress(self, event=None):
        self.key_pressed = event.keysym.lower()
        self.time_pressed = time.time()

        if self.key_pressed in ['left', 'right', 'up', 'down']:
            self.after(5, self.advance)

    def tkKeyRelease(self, event=None):
        self.key_pressed = None

    def advance(self, event=None):
        if self.key_pressed is None:
            return

        self.glView.draw()
        t = time.time()

        delta = 0.1 * (t - self.time_pressed)

        if self.key_pressed == 'left':
            self.glView.x -= delta
        if self.key_pressed == 'right':
            self.glView.x += delta
        if self.key_pressed == 'up':
            self.glView.y += delta
        if self.key_pressed == 'down':
            self.glView.y -= delta

        self.time_pressed = t
        self.after(5, self.advance)

if __name__ == '__main__':

    window = Window()

    if separate_slider:
        sliderWindow = tkinter.Tk()
        slider = ttk.Scale(master=sliderWindow,
                           orient=tkinter.HORIZONTAL,
                           command=window.glView.set_size)
        slider.grid(row=0, column=0, sticky=tkinter.NSEW)

    print("Using OpenGL", window.square_widget.gl_version())

    window.mainloop()

