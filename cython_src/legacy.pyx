# cython: language_level=3str

#This is obviously incomplete.  So far it is just a proof-of-concept.

cimport legacy as gl

GL_COLOR_BUFFER_BIT = gl.GL_COLOR_BUFFER_BIT
GL_QUADS = gl.GL_QUADS
GL_NO_ERROR = gl.GL_NO_ERROR

def glGetError():
    return gl.glGetError()
    
def glClearColor(gl.GLclampf red, gl.GLclampf green, gl.GLclampf blue, gl.GLclampf alpha):
    gl.glClearColor(red, green, blue, alpha)

def glClear(gl.GLbitfield mask):
    gl.glClear(mask)

def glViewport(gl.GLint x, gl.GLint y, gl.GLsizei width, gl.GLsizei height):
    gl.glViewport(x, y, width, height)
    
def glBegin(gl.GLenum mode):
    gl.glBegin(mode)
    
def glEnd():
    gl.glEnd()

def glVertex2d(gl.GLdouble x, gl.GLdouble y):
    gl.glVertex2d(x, y)

