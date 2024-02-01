from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os
import sys
import platform

OpenGL_includes = []
OpenGL_extra_compile_args = []
OpenGL_extra_link_args = []

macOS_link_args = []

if sys.platform == 'darwin':
    OS_X_ver = int(platform.mac_ver()[0].split('.')[1])
    sdk_roots = [
        '/Library/Developer/CommandLineTools/SDKs',
        '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs'
         ]
    version_strings = [ 'MacOSX10.%d.sdk' % OS_X_ver, 'MacOSX.sdk' ]
    poss_roots = [ '' ] + [
        '%s/%s' % (sdk_root, version_string)
        for sdk_root in sdk_roots
        for version_string in version_strings ]
    header_dir = '/System/Library/Frameworks/OpenGL.framework/Versions/Current/Headers/'
    poss_includes = [ root + header_dir for root in poss_roots ]
    OpenGL_includes += [ path for path in poss_includes if os.path.exists(path)][:1]
    OpenGL_extra_link_args = ['-framework', 'OpenGL']
    OpenGL_extra_link_args += macOS_link_args

if sys.platform == 'win32':
    OpenGL_extra_link_args = ['opengl32.lib']

extensions = cythonize(
    Extension(
        "tkinter_gl.legacy",
        ["cython_src/legacy.pyx"],
        include_dirs=OpenGL_includes,
        extra_link_args=OpenGL_extra_link_args,
        )
    )

setup(
    ext_modules = extensions
)
