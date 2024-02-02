import tkinter
from tkinter import ttk
from tkinter_gl import GLCanvas
from OpenGL.GL import (glClear, glClearColor, glBegin, glEnd,
    glVertex2d, glViewport, glGetError)
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_QUADS, GL_NO_ERROR
import time

class SquareWidget(GLCanvas):
    def __init__(self, parent):
        super().__init__(parent)

        self.size = 0.5
        self.x = 0.0
        self.y = 0.0

    def draw(self):
        self.make_current()
 
        glViewport(0, 0, self.winfo_width(), self.winfo_height())

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_QUADS)
        glVertex2d( self.x + self.size,  self.y + self.size)
        glVertex2d( self.x + self.size,  self.y - self.size)
        glVertex2d( self.x - self.size,  self.y - self.size)
        glVertex2d( self.x - self.size,  self.y + self.size)
        glEnd()

        while True:
            err = glGetError()
            if err == GL_NO_ERROR:
                break
            print("Error: ", err)

        self.swap_buffers()

class Window(tkinter.Toplevel):
    def __init__(self):
        super().__init__()

        self.key_pressed = None
        self.time_pressed = 0

        # On X11 at least, putting the TkGL widget in a frame
        # avoids some layout issues.

        label = ttk.Label(self, padding=(20, 0, 20, 0),
                          text="Use cursor keys to move square")
        frame = ttk.Frame(self)
        self.square_widget = SquareWidget(frame)
        
        label.pack(fill='x')
        frame.pack(expand=1, fill="both")
        self.square_widget.pack(expand=1, fill="both")
        
        self.bind('<KeyPress>', self.handle_key_press)
        self.bind('<KeyRelease>', self.handle_key_release)

        self.update()

    def set_size(self, value):
        self.square_widget.size = float(value)
        self.square_widget.draw()

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

        self.square_widget.draw()
        t = time.time()

        delta = 0.1 * (t - self.time_pressed)

        if self.key_pressed == 'left':
            self.square_widget.x -= delta
        if self.key_pressed == 'right':
            self.square_widget.x += delta
        if self.key_pressed == 'up':
            self.square_widget.y += delta
        if self.key_pressed == 'down':
            self.square_widget.y -= delta

        self.time_pressed = t
        self.after(5, self.advance)

if __name__ == '__main__':

    root = tkinter.Tk()
    window = Window()

    root.geometry('300x50+600+100')

    label = ttk.Label(root, text="Zoom: ", padding=(10, 0, 0, 0))
    label.grid(row=0, column=0)
    
    slider = ttk.Scale(root,
                       orient=tkinter.HORIZONTAL,
                       command=window.set_size,
                       value=window.square_widget.size)
    slider.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')
    root.columnconfigure(1, weight=1)

    print("Using OpenGL", window.square_widget.gl_version())

    root.mainloop()

