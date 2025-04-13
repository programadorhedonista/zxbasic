	org 32768
.core.__START_PROGRAM:
	di
	push ix
	push iy
	exx
	push hl
	exx
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
	DEFB 00
.core.ZXBASIC_USER_DATA_END:
.core.__MAIN_PROGRAM__:
.LABEL._5:
.LABEL._10:
	ld h, 1
	ld a, (_a)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL0
	ld hl, _a
	inc (hl)
.LABEL._20:
	jp .LABEL.__LABEL1
.LABEL.__LABEL0:
	xor a
	ld hl, (_a - 1)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL3
	xor a
	ld (_a), a
.LABEL._30:
.LABEL.__LABEL3:
.LABEL.__LABEL1:
.LABEL._40:
	ld h, 1
	ld a, (_a)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL4
	ld hl, _a
	inc (hl)
.LABEL._50:
	jp .LABEL.__LABEL5
.LABEL.__LABEL4:
	xor a
	ld hl, (_a - 1)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL6
	xor a
	ld (_a), a
	jp .LABEL.__LABEL7
.LABEL.__LABEL6:
	ld a, (_a)
	or a
	jp nz, .LABEL.__LABEL9
	ld a, 255
	ld (_a), a
.LABEL._60:
.LABEL.__LABEL9:
.LABEL.__LABEL7:
.LABEL.__LABEL5:
	ld h, 1
	ld a, (_a)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL10
	ld hl, _a
	inc (hl)
	jp .LABEL.__LABEL11
.LABEL.__LABEL10:
	xor a
	ld hl, (_a - 1)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL13
	xor a
	ld (_a), a
.LABEL.__LABEL13:
.LABEL.__LABEL11:
	ld h, 1
	ld a, (_a)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL14
	ld hl, _a
	inc (hl)
	jp .LABEL.__LABEL15
.LABEL.__LABEL14:
	xor a
	ld hl, (_a - 1)
	call .core.__LTI8
	or a
	jp z, .LABEL.__LABEL16
	xor a
	ld (_a), a
	jp .LABEL.__LABEL17
.LABEL.__LABEL16:
	ld a, (_a)
	or a
	jp nz, .LABEL.__LABEL19
	ld a, 255
	ld (_a), a
.LABEL.__LABEL19:
.LABEL.__LABEL17:
.LABEL.__LABEL15:
	ld hl, 0
	ld b, h
	ld c, l
.core.__END_PROGRAM:
	di
	ld hl, (.core.__CALL_BACK__)
	ld sp, hl
	exx
	pop hl
	exx
	pop iy
	pop ix
	ei
	ret
	;; --- end of user code ---
#line 1 "/zxbasic/src/lib/arch/zx48k/runtime/cmp/lti8.asm"
#line 1 "/zxbasic/src/lib/arch/zx48k/runtime/cmp/lei8.asm"
	    push namespace core
__LEI8: ; Signed <= comparison for 8bit int
	    ; A <= H (registers)
	    PROC
	    LOCAL checkParity
	    sub h
	    jr nz, __LTI
	    inc a
	    ret
__LTI8:  ; Test 8 bit values A < H
	    sub h
__LTI:   ; Generic signed comparison
	    jp po, checkParity
	    xor 0x80
checkParity:
	    ld a, 0     ; False
	    ret p
	    inc a       ; True
	    ret
	    ENDP
	    pop namespace
#line 2 "/zxbasic/src/lib/arch/zx48k/runtime/cmp/lti8.asm"
#line 112 "arch/zx48k/ifthenelseif.bas"
	END
