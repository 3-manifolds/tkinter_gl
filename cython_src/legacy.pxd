#This is obviously incomplete.  So far it is just a proof-of-concept.

cdef extern from "gl_headers.h":
    ctypedef unsigned int GLenum
    ctypedef unsigned char GLboolean
    ctypedef unsigned int GLbitfield
    ctypedef void GLvoid
    ctypedef signed char GLbyte
    ctypedef short GLshort
    ctypedef int GLint
    ctypedef unsigned char GLubyte
    ctypedef unsigned short GLushort
    ctypedef unsigned int GLuint
    ctypedef int GLsizei
    ctypedef float GLfloat
    ctypedef float GLclampf
    ctypedef double GLdouble
    ctypedef double GLclampd
    ctypedef char GLchar
    ctypedef void* GLintptr
    ctypedef void* GLsizeiptr

    enum:
        GL_COLOR_BUFFER_BIT
        GL_QUADS
        GL_NO_ERROR

    GLenum glGetError()
    void glClearColor(GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha )
    void glClear(GLbitfield mask )
    void glViewport(GLint x, GLint y, GLsizei width, GLsizei height)
    void glBegin(GLenum mode)
    void glEnd()
    void glVertex2d(GLdouble x, GLdouble y )
    
