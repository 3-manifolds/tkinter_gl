"""
Shows a dial spinning once per second as an example of a simple animation.
"""

import tkinter
from tkinter import ttk
from tkinter_gl import GLCanvas
import time
import sys

try:
    from OpenGL import GL
except ImportError:
    raise ImportError(
        """
        This example requires PyOpenGL.

        You can install it with "pip install PyOpenGL".
        """)

class ClockWidget(GLCanvas):
    profile = 'legacy'

    dial_length = 0.8
    dial_counterlength = 0.1
    dial_width = 0.05
    
    def __init__(self, parent):
        super().__init__(parent)

        self.start_time = time.time()

        self.is_first_draw = True

    def draw(self):
        self.make_current()
 
        GL.glViewport(0, 0, self.winfo_width(), self.winfo_height())

        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        angle = -360.0 * (time.time() - self.start_time)
        
        GL.glRotatef(angle, 0, 0, 1)
        
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2d(  self.dial_width,  self.dial_length)
        GL.glVertex2d(  self.dial_width, -self.dial_counterlength)
        GL.glVertex2d( -self.dial_width, -self.dial_counterlength)
        GL.glVertex2d( -self.dial_width,  self.dial_length)
        GL.glEnd()

        while True:
            err = GL.glGetError()
            if err == GL.GL_NO_ERROR:
                break
            print("Error: ", err)

        self.swap_buffers()

        if self.is_first_draw:
            self.is_first_draw = False
            self.after(5, self.animate)

    def animate(self):
        self.draw()

        # We schedule a redraw almost immediately.
        #
        # Specifying a delay of 0 can cause a non-responsive
        # application on some operating systems.
        self.after(5, self.animate)

if __name__ == '__main__':
    root = tkinter.Tk()
    widget = ClockWidget(root)
    print("Using OpenGL", widget.gl_version())
    widget.pack(expand=True, fill='both', padx=50, pady=50)
    root.mainloop()

