#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4:et:sw=4:

# ----------------------------------------------------------------------
# Copyleft (K), Jose M. Rodriguez-Rosa (a.k.a. Boriel)
#
# This program is Free Software and is released under the terms of
#                    the GNU General License
# ----------------------------------------------------------------------

from typing import List

from src.api import global_
from src.api.config import OPTIONS
from src.api.constants import SCOPE
from src.api.constants import CLASS

from .symbol_ import Symbol


# ----------------------------------------------------------------------
# Identifier Symbol object
# ----------------------------------------------------------------------


class SymbolID(Symbol):
    """Defines a generic ID"""

    _class: CLASS = CLASS.unknown

    def __init__(self, name: str, lineno: int, class_: CLASS = CLASS.unknown, *children: List[Symbol]):
        super().__init__(*children)
        self.name = name
        self.filename = global_.FILENAME  # In which file was first used
        self.lineno = lineno  # In which line was first used
        self.class_ = class_  # variable "class": var, label, function, etc.
        self.mangled = f"{global_.MANGLE_CHR}{name}"  # This value will be overridden later
        self.declared = False  # if explicitly declared (DIM var AS <type>)
        self.referred_by: List[Symbol] = []  # list of symbols using this one

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ID:%s" % str(self)

    @property
    def is_required(self) -> bool:
        return len(self.referred_by) > 0
