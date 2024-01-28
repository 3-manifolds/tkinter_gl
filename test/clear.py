import tkinter
from tkinter_gl import GLViewBase
from OpenGL import GL

class GLView(GLViewBase):
    def __init__(self, parent, cnf={}, **kw):
        GLViewBase.__init__(self, parent, cnf, **kw)
        self.bind('<Enter>', lambda event: self.draw(color='blue'))
        self.bind('<Leave>', lambda event: self.draw(color='purple'))
        
    def draw(self, color='blue'):
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
surface.pack()
root.mainloop()

    
