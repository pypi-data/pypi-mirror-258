import os
import sys
from dektools.file import read_text
from .constants import dir_name_venv


def activate_venv(path_venv=None, ignore=False):
    this_file = os.path.join(os.path.abspath(path_venv or dir_name_venv), 'Scripts', 'activate_this.py')
    if not ignore or os.path.isfile(this_file):
        exec(read_text(this_file), {'__file__': this_file})


def is_venv_active(sp=None):
    return (sp or sys.prefix) != sys.base_prefix
