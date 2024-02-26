# copyright ############################### #
# This file is part of the Xaux Package.    #
# Copyright (c) CERN, 2024.                 #
# ######################################### #

import os, subprocess
from pathlib import Path
from time import sleep
import random


def on_afs(file):
    parents = list(fs_path(file).parents)
    if len(parents) < 3:
        return False
    else:
        return parents[-3] == Path('/afs/cern.ch')

def afs_accessible():
    return Path('/afs/cern.ch').exists()


def fs_path(path):
    path = Path(path).expanduser().resolve()
    return Path(path.as_posix().replace('/eos/home-','/eos/user/'))

class FsPath(Path):
    _flavour = type(Path())._flavour

    def __new__(cls, *args, **kwargs):
        if cls is FsPath:
            cls = EosPath if else 
        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError("cannot instantiate %r on your system"
                                      % (cls.__name__,))
        self._init()
        return self

    def __init__(*args, **kwargs():
        self.path = Path(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.path, attr)

    @property
    def on_afs(self):
        if not hasattr(self, '_domain'):
            parents = list(fs_path(file).parents)
    if len(parents) < 3:
        return False
    else:
        return parents[-3] == Path('/afs/cern.ch')

    @property
    def on_eos(file):
        parents = list(fs_path(file).parents)
        if len(parents) < 2:
            return False
        else:
            return parents[-2] == Path('/eos')
