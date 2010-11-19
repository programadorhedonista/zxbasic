#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# Copyleft (k) 2008, by Jose M. Rodriguez-Rosa
# (a.k.a. Boriel, http://www.boriel.com)
#
# This module contains array load/store
# intermediate-code traductions
# --------------------------------------------------------------

from __common import REQUIRES, is_float
from __f16 import f16, _f16_oper
from __float import _float, _fpop, _fpush, _float_oper

def _addr(value):
	''' Common subroutine for emmiting array address
	'''
	output = []

	try:
		indirect = False
		if value[0] == '*':
			indirect = True
			value = value[1:]

		value = int(value) & 0xFFFF
		if indirect:
			output.append('ld hl, (%s)' % str(value))
		else:
			output.append('ld hl, %s' % str(value))

	except ValueError:
		if value[0] == '_':
			output.append('ld hl, %s' % str(value))
			if indirect:
				output.append('ld c, (hl)')
				output.append('inc hl')
				output.append('ld h, (hl)')
				output.append('ld l, c')
		else:
			output.append('pop hl')
			if indirect:
				output.append('ld c, (hl)')
				output.append('inc hl')
				output.append('ld h, (hl)')
				output.append('ld l, c')

	output.append('call __ARRAY')
	REQUIRES.add('array.asm')
	
	return output



def _aaddr(ins):
	''' Loads the address of an array element
	into the stack.
	'''
	output = _addr(ins.quad[2])
	output.append('push hl')

	return output


def _aload8(ins):
	''' Loads an 8 bit value from a memory address
	If 2nd arg. start with '*', it is always treated as
	an indirect value.
	'''
	output = _addr(ins.quad[2])
	output.append('ld a, (hl)')
	output.append('push af')

	return output



def _aload16(ins):
	''' Loads a 16 bit value from a memory address
	If 2nd arg. start with '*', it is always treated as
	an indirect value.
	'''
	output = _addr(ins.quad[2])
	
	output.append('ld e, (hl)')
	output.append('inc hl')
	output.append('ld d, (hl)')
	output.append('ex de, hl')
	output.append('push hl')

	return output


def _aload32(ins):
	''' Load a 32 bit value from a memory address
	If 2nd arg. start with '*', it is always treated as
	an indirect value.
	'''
	output = _addr(ins.quad[2])

	output.append('call __ILOAD32')
	output.append('push de')
	output.append('push hl')

	REQUIRES.add('iload32.asm')

	return output



def _aloadf(ins):
	''' Loads a floating point value from a memory address.
	If 2nd arg. start with '*', it is always treated as
	an indirect value.
	'''
	output = _addr(ins.quad[2])
	output.append('call __LOADF')
	output.extend(_fpush())

	REQUIRES.add('iloadf.asm')

	return output



def _aloadstr(ins):
	''' Loads a string value from a memory address.
	'''
	output = _addr(ins.quad[2])

	output.append('call __ILOADSTR')
	output.append('push hl')
	REQUIRES.add('loadstr.asm')

	return output
		


def _astore8(ins):
	''' Stores 2º operand content into address of 1st operand.
	1st operand is an array element. Dimensions are pushed into the 
	stack.
	Use '*' for indirect store on 1st operand (A pointer to an array)
	'''
	output = _addr(ins.quad[1])

	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	try:
		value = int(ins.quad[2]) & 0xFFFF
		if indirect:
			output.append('ld a, (%i)' % value)
			output.append('ld (hl), a')
		else:
			value &= 0xFF
			output.append('ld (hl), %i' % value)
	except ValueError:
		output.append('pop af')
		output.append('ld (hl), a')

	return output



def _astore16(ins):
	''' Stores 2º operand content into address of 1st operand.
	store16 a, x =>  *(&a) = x
	Use '*' for indirect store on 1st operand.
	'''
	output = _addr(ins.quad[1])

	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	try:
		value = int(ins.quad[2]) & 0xFFFF
		output.append('ld de, %i' % value)
		if indirect:
			output.append('call __LOAD_DE_DE')
			REQUIRES.add('lddede.asm')

	except ValueError:
		output.append('pop de')

	output.append('ld (hl), e')
	output.append('inc hl')
	output.append('ld (hl), d')

	return output



def _astore32(ins):
	''' Stores 2º operand content into address of 1st operand.
	store16 a, x =>  *(&a) = x
	'''
	output = _addr(ins.quad[1])

	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	try:
		value = int(ins.quad[2]) & 0xFFFFFFFF # Immediate?
		if indirect:
			output.append('push hl')
			output.append('ld hl, %i' % (value & 0xFFFF))
			output.append('call __ILOAD32')
			output.append('ld b, h')
			output.append('ld c, l') # BC = Lower 16 bits
			output.append('pop hl')
			REQUIRES.add('iload32.asm')
		else:
			output.append('ld de, %i' % (value >> 16))
			output.append('ld bc, %i' % (value & 0xFFFF))
	except ValueError:
		output.append('pop bc')
		output.append('pop de')

	output.append('call __STORE32')
	REQUIRES.add('store32.asm')

	return output



def _astoref16(ins):
	''' Stores 2º operand content into address of 1st operand.
	storef16 a, x =>  *(&a) = x
	'''
	output = _addr(ins.quad[1])

	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	if indirect:
		output.append('push hl')
		output.extend(_f16_oper(ins.quad[2], useBC = True))
		output.append('pop hl')
		REQUIRES.add('iload32.asm')
	else:
		output.extend(_f16_oper(ins.quad[2], useBC = True))

	output.append('call __STORE32')
	REQUIRES.add('store32.asm')

	return output



def _astoref(ins):
	''' Stores a floating point value into a memory address.
	'''
	output = _addr(ins.quad[1])

	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	if indirect:
		output.append('push hl')
		output.extend(_float_oper(ins.quad[2]))
		output.append('pop hl')
	else:
		output.extend(_float_oper(ins.quad[2]))

	output.append('call __STOREF')
	REQUIRES.add('storef.asm')

	return output



def _astorestr(ins):
	''' Stores a string value into a memory address.
	It copies content of 2nd operand (string), into 1st, reallocating
	dynamic memory for the 1st str. These instruction DOES ALLOW
	inmediate strings for the 2nd parameter, starting with '#'.
	'''
	output = _addr(ins.quad[1])

	temporal = False
	value = ins.quad[2]
	if value[0] == '*':
		value = value[1:]
		indirect = True
	else:
		indirect = False

	if value[0] == '_':
		output.append('ld de, (%s)' % value)

		if indirect:
			output.append('call __LOAD_DE_DE')
			REQUIRES.add('lddede.asm')

	elif value[0] == '#':
		output.append('ld de, %s' % value[1:])
	else:
		output.append('pop de')
		temporal = True
		if indirect:
			output.append('call __LOAD_DE_DE')
			REQUIRES.add('lddede.asm')

	if not temporal:
		output.append('call __STORE_STR')
		REQUIRES.add('storestr.asm')
	else: # A value already on dynamic memory
		output.append('call __STORE_STR2')
		REQUIRES.add('storestr2.asm')

	return output



