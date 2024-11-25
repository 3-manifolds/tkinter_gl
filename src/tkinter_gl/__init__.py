import os
import sys
import tkinter
__version__ = '1.0b2'

class GLCanvas(tkinter.Widget, tkinter.Misc):
    """
    A Tk widget which provides an OpenGL rendering surface.

    Clients should subclass from GLCanvas and implement draw.

    To specify an OpenGL version, the subclass should override GLCanvas.profile
    to "legacy", "3_2" or "4_1".

    "legacy" requests OpenGL version 2.1 from the OS. The OS will produce
    an OpenGL context supporting the fixed function pipeline and legacy calls
    such as glBegin/glEnd.

    "3_2" and "4_1" requests OpenGL version 3.2 or 4.1, respectively, from the
    OS. The OS will produce an OpenGL context supporting shaders of a version
    later than the one request.

    Note that we do not have a flag to (explicitly) request a compatibility
    context supporting both legacy calls such as glBegin/glEnd as well as
    shaders (the reason is that Mac OS X does not provide API for such a
    request).

    See https://github.com/3-manifolds/tkinter_gl/tree/main/test for examples.
    """

    # Set to "legacy" (default, for OpenGL 2.1), "3_2", or "4_1"
    profile = ''

    def __init__(self, parent, cnf={}, **kw):
        if sys.platform == 'win32':
            # Make sure the parent has been mapped.
            parent.update()
        pkg_dir = os.path.join(__path__[0], 'tk', sys.platform,)
        if not os.path.exists(pkg_dir):
            raise RuntimeError('TkGL package directory "%s" is missing.' % pkg_dir)
        parent.tk.call('lappend', 'auto_path', pkg_dir)
        parent.tk.call('package', 'require', 'Tkgl')
        if self.profile:
            kw['profile'] = self.profile
        tkinter.Widget.__init__(self, parent, 'tkgl', cnf, kw)
        self.bind('<Expose>', self._handle_expose)
        self.bind('<Map>', self._handle_map)

        # Make sure the handler is installed.
        self.update_idletasks()

    def gl_version(self):
        """
        The result of glGetString(GL_VERSION).
        """
        return self.tk.call(self._w, 'glversion')

    def gl_extensions(self):
        return self.tk.call(self._w, 'extensions')

    def make_current(self):
        """
        Makes the OpenGL context for this GLCanvas the current context.
        """
        self.tk.call(self._w, 'makecurrent')

    def swap_buffers(self):
        """
        Makes back buffer (which we draw to by default) be displayed
        in GLCanvas.
        """
        self.tk.call(self._w, 'swapbuffers')

    def draw(self):
        """
        Draw the scene.

        Subclasses override this method to make GL calls.
        """

    def _handle_expose(self, event):
        self.after_idle(self.draw)

    def _handle_map(self, event):
        self.after_idle(self.draw)
