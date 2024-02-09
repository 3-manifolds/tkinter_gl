import os
import sys
import tkinter
__version__ = '1.0a2'

class GLCanvas(tkinter.Widget, tkinter.Misc):
    """
    A Tk widget which provides an OpenGL rendering surface.
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
        return self.tk.call(self._w, 'glversion')

    def gl_extensions(self):
        return self.tk.call(self._w, 'extensions')

    def make_current(self):
        self.tk.call(self._w, 'makecurrent')

    def swap_buffers(self):
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
