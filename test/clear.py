import tkinter
from tkinter_gl import GLWidget
from OpenGL import GL

class GLView(GLWidget):
    def __init__(self, parent, cnf={}, **kw):
        super().__init__(parent, cnf, **kw)
        self.bind('<Enter>', lambda event: self.draw_impl(color='blue'))
        self.bind('<Leave>', lambda event: self.draw_impl(color='purple'))

    def draw(self):
        if (0 <= self.winfo_pointerx() < self.winfo_width() and
            0 <= self.winfo_pointery() < self.winfo_height()):
            self.draw_impl(color = 'blue')
        else:
            self.draw_impl(color = 'purple')

    def draw_impl(self, color):
        self.make_current()
        if color == 'blue':
            GL.glClearColor(0.0, 0, 1.0, 1.0)
        elif color == 'purple':
            GL.glClearColor(1.0, 0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.swap_buffers()

if __name__ == '__main__':
    root = tkinter.Tk()
    surface = GLView(root)
    print("Using OpenGL", surface.gl_version())
    surface.pack(expand=True, fill='both')
    root.mainloop()

    
