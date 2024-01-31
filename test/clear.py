import tkinter
from tkinter_gl import GLWidget
from OpenGL import GL

class GLView(GLWidget):
    def __init__(self, parent, cnf={}, **kw):
        super().__init__(parent, cnf, **kw)
        self.bind('<Enter>', lambda event: self.draw(color='blue'))
        self.bind('<Leave>', lambda event: self.draw(color='purple'))
        
    def draw(self, color=None):
        if color is None:
            if (0 <= self.winfo_pointerx() < self.winfo_width() and
                0 <= self.winfo_pointery() < self.winfo_height()):
                color = 'blue'
            else:
                color = 'purple'
        self.make_current()
        if color == 'blue':
            GL.glClearColor(0.0, 0, 1.0, 1.0)
        elif color == 'purple':
            GL.glClearColor(1.0, 0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.swap_buffers()
        
root = tkinter.Tk()
surface = GLView(root)
print("Using OpenGL", surface.gl_version())
surface.pack(expand=True, fill='both')
root.mainloop()

    
