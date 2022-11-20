#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4:et:sw=4:

# ----------------------------------------------------------------------
# Copyleft (K), Jose M. Rodriguez-Rosa (a.k.a. Boriel)
#
# This program is Free Software and is released under the terms of
#                    the GNU General License
# ----------------------------------------------------------------------

import numbers
from typing import Optional

from src.api.constants import CLASS
from src.symbols.constexpr import SymbolCONSTEXPR
from src.symbols.symbol_ import Symbol
from src.symbols.type_ import SymbolTYPE
from src.symbols.type_ import Type as TYPE


def _get_val(other):
    """Given a Number, a Numeric Constant or a python number return its value"""
    assert isinstance(other, (numbers.Number, SymbolNUMBER, SymbolCONSTEXPR))
    if isinstance(other, SymbolNUMBER):
        return other.value

    if isinstance(other, SymbolCONSTEXPR):
        return other.expr.value

    return other


class SymbolNUMBER(Symbol):
    """Defines an NUMBER symbol."""

    def __init__(self, value, lineno: int, type_: Optional[SymbolTYPE] = None):
        assert lineno is not None
        assert type_ is None or isinstance(type_, SymbolTYPE)

        if isinstance(value, SymbolNUMBER):
            value = value.value

        assert isinstance(value, numbers.Number)
        super().__init__()
        self.class_ = CLASS.const

        if int(value) == value:
            value = int(value)
        else:
            value = float(value)

        self.value = value

        if type_ is not None:
            self.type_ = type_

        elif isinstance(value, float):
            if -32768.0 < value < 32767:
                self.type_ = TYPE.fixed
            else:
                self.type_ = TYPE.float_

        elif isinstance(value, int):
            if 0 <= value < 256:
                self.type_ = TYPE.ubyte
            elif -128 <= value < 128:
                self.type_ = TYPE.byte_
            elif 0 <= value < 65536:
                self.type_ = TYPE.uinteger
            elif -32768 <= value < 32768:
                self.type_ = TYPE.integer
            elif value < 0:
                self.type_ = TYPE.long_
            else:
                self.type_ = TYPE.ulong

        self.lineno = lineno

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "%s:%s" % (self.type_, str(self))

    def __hash__(self):
        return id(self)

    @property
    def t(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, (numbers.Number, SymbolNUMBER, SymbolCONSTEXPR)):
            return False

        return self.value == _get_val(other)

    def __lt__(self, other):
        return self.value < _get_val(other)

    def __le__(self, other):
        return self.value <= _get_val(other)

    def __gt__(self, other):
        return self.value > _get_val(other)

    def __ge__(self, other):
        return self.value >= _get_val(other)

    def __add__(self, other):
        return SymbolNUMBER(self.value + _get_val(other), self.lineno)

    def __radd__(self, other):
        return SymbolNUMBER(_get_val(other) + self.value, self.lineno)

    def __sub__(self, other):
        return SymbolNUMBER(self.value - _get_val(other), self.lineno)

    def __rsub__(self, other):
        return SymbolNUMBER(_get_val(other) - self.value, self.lineno)

    def __mul__(self, other):
        return SymbolNUMBER(self.value * _get_val(other), self.lineno)

    def __rmul__(self, other):
        return SymbolNUMBER(_get_val(other) * self.value, self.lineno)

    def __truediv__(self, other):
        return SymbolNUMBER(self.value / _get_val(other), self.lineno)

    def __div__(self, other):
        return self.__truediv__(other)

    def __rtruediv__(self, other):
        return SymbolNUMBER(_get_val(other) / self.value, self.lineno)

    def __rdiv__(self, other):
        return self.__rtruediv__(other)

    def __or__(self, other):
        return SymbolNUMBER(self.value | _get_val(other), self.lineno)

    def __ror__(self, other):
        return SymbolNUMBER(_get_val(other | self.value), self.lineno)

    def __and__(self, other):
        return SymbolNUMBER(self.value & _get_val(other), self.lineno)

    def __rand__(self, other):
        return SymbolNUMBER(_get_val(other) & self.value, self.lineno)

    def __mod__(self, other):
        return SymbolNUMBER(self.value % _get_val(other), self.lineno)

    def __rmod__(self, other):
        return SymbolNUMBER(_get_val(other) % self.value, self.lineno)
