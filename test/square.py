"""
Shows a square that can be moved with the cursor keys and whose size
can be controlled by a slider.

Shows how to do "animation", that is repeatedly calling draw using the
elapsed time to compute how far the square has moved. Also tests that
we correctly update the GLCanvas to slider events.
"""

import tkinter
from tkinter import ttk
from tkinter_gl import GLCanvas
import time
import sys
import os

try:
    import OpenGL
    from OpenGL import GL
except ImportError:
    raise ImportError(
        """
        This example requires PyOpenGL.

        You can install it with "pip install PyOpenGL".
        """)

class SquareWidget(GLCanvas):
    profile = 'legacy'
    
    def __init__(self, parent):
        super().__init__(parent)
        self.make_current()

        self.size = 0.5

        # Position of square.
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

    def set_size(self, value):
        self.square_widget.size = float(value)
        self.square_widget.draw()

    def handle_key_press(self, event):
        # Record key and time to do the "animation"
        self.key_pressed = event.keysym.lower()
        self.time_pressed = time.time()

        # Start animation by scheduling the initial call to
        # self.animate (which will keep scheduling itself as
        # long as a key is pressed).
        if self.key_pressed in ['left', 'right', 'up', 'down']:
            self.after(5, self.animate)

    def handle_key_release(self, event):
        self.key_pressed = None

    def animate(self):
        if self.key_pressed is None:
            # Stop when key was released
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
        # We schedule a redraw almost immediately.
        #
        # Specifying a delay of 0 can cause a non-responsive
        # application on some operating systems.
        self.after(5, self.animate)

if __name__ == '__main__':

    root = tkinter.Tk()
    # Make it big enoush so that its close button is visible.
    root.geometry('600x75+600+100')

    label = ttk.Label(root, text="Square size: ", padding=(10, 0, 0, 0))
    label.grid(row=0, column=0)
    
    slider = ttk.Scale(root, orient=tkinter.HORIZONTAL)
    slider.grid(row=0, column=1, padx=20, pady=30, sticky='nsew')
    root.columnconfigure(1, weight=1)

    window = Window()
    slider.configure(command=window.set_size,
                     value=window.square_widget.size)
    print("Using OpenGL", window.square_widget.gl_version())
    root.mainloop()
