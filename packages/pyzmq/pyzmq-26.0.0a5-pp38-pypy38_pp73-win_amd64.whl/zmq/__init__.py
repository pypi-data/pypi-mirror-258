"""Python bindings for 0MQ"""


# start delvewheel patch
def _delvewheel_patch_1_5_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyzmq.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyzmq-26.0.0a5')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pyzmq-26.0.0a5')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_5_2()
del _delvewheel_patch_1_5_2
# end delvewheel patch

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.

import os
import sys
from contextlib import contextmanager


@contextmanager
def _libs_on_path():
    """context manager for libs directory on $PATH

    Works around mysterious issue where os.add_dll_directory
    does not resolve imports (conda-forge Python >= 3.8)
    """

    if not sys.platform.startswith("win"):
        yield
        return

    libs_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            "pyzmq.libs",
        )
    )
    if not os.path.exists(libs_dir):
        # no bundled libs
        yield
        return

    path_before = os.environ.get("PATH")
    try:
        os.environ["PATH"] = os.pathsep.join([path_before or "", libs_dir])
        yield
    finally:
        if path_before is None:
            os.environ.pop("PATH")
        else:
            os.environ["PATH"] = path_before


# zmq top-level imports

# workaround for Windows
with _libs_on_path():
    from zmq import backend

from . import constants  # noqa
from .constants import *  # noqa
from zmq.backend import *  # noqa
from zmq import sugar
from zmq.sugar import *  # noqa


def get_includes():
    """Return a list of directories to include for linking against pyzmq with cython."""
    from os.path import abspath, dirname, exists, join, pardir

    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    includes = [parent] + [join(parent, base, subdir) for subdir in ('utils',)]
    if exists(join(parent, base, 'include')):
        includes.append(join(parent, base, 'include'))
    return includes


def get_library_dirs():
    """Return a list of directories used to link against pyzmq's bundled libzmq."""
    from os.path import abspath, dirname, join, pardir

    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    return [join(parent, base)]


COPY_THRESHOLD = 65536
DRAFT_API = backend.has("draft")

__all__ = (
    [
        'get_includes',
        'COPY_THRESHOLD',
        'DRAFT_API',
    ]
    + constants.__all__
    + sugar.__all__
    + backend.__all__
)