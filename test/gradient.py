"""
Draws a gradient to show how to use shaders.
"""

import tkinter
from tkinter_gl import GLCanvas
import struct
import sys

try:
    import OpenGL
    if sys.platform == 'linux':
        # PyOpenGL is broken with wayland:
        OpenGL.setPlatform('x11')
    from OpenGL import GL
except ImportError:
    raise ImportError(
        """
        This example requires PyOpenGL.

        You can install it with "pip install PyOpenGL".
        """)

class GLView(GLCanvas):
    profile = '4_1'
    
    def __init__(self, parent, cnf={}, **kw):
        super().__init__(parent, cnf, **kw)
        self.initialized = False
        self.make_current()

    def draw(self):
        self.make_current()
        if not self.initialized:
            vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
            GL.glShaderSource(
                vertex_shader,
                [ """
                #version 150

                in vec4 position;

                void main()
                {
                    gl_Position = position;
                }
                """])
            GL.glCompileShader(vertex_shader)
            if not GL.glGetShaderiv(vertex_shader, GL.GL_COMPILE_STATUS):
                raise RuntimeError("Could not compile vertex shader")

            fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
            GL.glShaderSource(
                fragment_shader,
                [ """
                #version 150

                uniform vec2 windowSize;

                out vec4 out_FragColor;

                void main() {
                    out_FragColor = vec4(gl_FragCoord.xy / windowSize, 0.0, 1.0);
                }
                """ ])
            GL.glCompileShader(fragment_shader)
            if not GL.glGetShaderiv(fragment_shader, GL.GL_COMPILE_STATUS):
                raise RuntimeError("Could not compile fragment shader")

            self.program = GL.glCreateProgram()
            GL.glAttachShader(self.program, vertex_shader)
            GL.glAttachShader(self.program, fragment_shader)
            GL.glLinkProgram(self.program)

            if not GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS):
                raise RuntimeError("Could not link shader")

            self.vao = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.vao)

            self.vbo = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
            # 6 floats for 3 2-vectors
            #
            # They form the vertices of a triangle that is large enough to
            # cover the entire window.
            GL.glBufferData(GL.GL_ARRAY_BUFFER,
                            struct.pack('=ffffff',
                                        3.0, -1.0,
                                        -1.0, 3.0,
                                        -1.0, -1.0),
                            GL.GL_STATIC_DRAW)

            self.initialized = True

        width = self.winfo_width()
        height = self.winfo_height()
        
        GL.glViewport(0, 0, width, height)

        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glEnableVertexAttribArray(0)
        
        GL.glVertexAttribPointer(0, # Data are for the first vertex attribute
                                    # Corresponds to "in vec4 position" in
                                    # vertex shader
                                 2, # We specify the first two coordinates x, y of
                                    # each vertex. OpenGL expands to (x,y,0,1)
                                 GL.GL_FLOAT, # Numeric type we provide
                                 GL.GL_FALSE, # No normalization
                                 2 * 4, # Stride. To get to the next vertex
                                        # in our buffer, we need to move to
                                        # floats forward, each float is 4 bytes.
                                 None) # pointer specifies offset.

        GL.glUseProgram(self.program)

        # Set values for "uniform vec2 windowSize" in fragment shader.
        l = GL.glGetUniformLocation(self.program, 'windowSize')
        GL.glUniform2f(l, width, height)

        # Consume three vertices to draw one triangle
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        self.swap_buffers()

if __name__ == '__main__':
    root = tkinter.Tk()
    surface = GLView(root)
    print("Using OpenGL", surface.gl_version())
    surface.pack(expand=True, fill='both', padx=50, pady=50)
    root.mainloop()

    
