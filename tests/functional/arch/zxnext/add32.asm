	org 32768
.core.__START_PROGRAM:
	di
	push iy
	ld iy, 0x5C3A  ; ZX Spectrum ROM variables address
	ld (.core.__CALL_BACK__), sp
	ei
	jp .core.__MAIN_PROGRAM__
.core.__CALL_BACK__:
	DEFW 0
.core.ZXBASIC_USER_DATA:
	; Defines USER DATA Length in bytes
.core.ZXBASIC_USER_DATA_LEN EQU .core.ZXBASIC_USER_DATA_END - .core.ZXBASIC_USER_DATA
	.core.__LABEL__.ZXBASIC_USER_DATA_LEN EQU .core.ZXBASIC_USER_DATA_LEN
	.core.__LABEL__.ZXBASIC_USER_DATA EQU .core.ZXBASIC_USER_DATA
_a:
	DEFB 00, 00, 00, 00
_b:
	DEFB 00, 00, 00, 00
.core.ZXBASIC_USER_DATA_END:
.core.__MAIN_PROGRAM__:
	ld hl, (_a)
	ld de, (_a + 2)
	ld (_b), hl
	ld (_b + 2), de
	ld de, 0
	ld hl, 1
	ld bc, (_a)
	add hl, bc
	ex de, hl
	ld bc, (_a + 2)
	adc hl, bc
	ex de, hl
	ld (_b), hl
	ld (_b + 2), de
	ld hl, (_a)
	ld de, (_a + 2)
	ld (_b), hl
	ld (_b + 2), de
	ld de, 0
	ld hl, 1
	ld bc, (_a)
	add hl, bc
	ex de, hl
	ld bc, (_a + 2)
	adc hl, bc
	ex de, hl
	ld (_b), hl
	ld (_b + 2), de
	ld hl, (_a)
	ld de, (_a + 2)
	ld bc, (_a)
	add hl, bc
	ex de, hl
	ld bc, (_a + 2)
	adc hl, bc
	ex de, hl
	ld (_b), hl
	ld (_b + 2), de
	ld hl, 0
	ld b, h
	ld c, l
.core.__END_PROGRAM:
	di
	ld hl, (.core.__CALL_BACK__)
	ld sp, hl
	pop iy
	ei
	ret
	;; --- end of user code ---
	END
