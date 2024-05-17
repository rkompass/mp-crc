# Optimization import for Micropython crc class.
#
# 8-bit table based right shift asm_thumb crc 8, 16 and 32 implementations

# --- internal ---
# r5 .. idx or tab[idx]
# r4 .. working and test register
# --- arguments ---
# r3 .. lookup table address
# r2 .. n (length of data)
# r1 .. data address
# r0 .. crc
@micropython.asm_thumb
def _crc8_tr(r0, r1, r2, r3) -> uint:
    label(loop)
    ldrb(r5, [r1, 0])  # idx = data[0]
    add(r1, 1)         # increment data pointer
    eor(r5, r0)        # idx ^= crc
    add(r5, r5, r3)    # table data address
    ldrb(r0, [r5, 0])  # fetch table entry: r0 = tab[idx]
    sub(r2, 1)         # n -= 1
    bne(loop)          # --- test and outer end ---

# --- internal ---
# r6 .. 0xff
# r5 .. idx or tab[idx]
# r4 .. working and test register
# --- arguments ---
# r3 .. lookup table address
# r2 .. n (length of data)
# r1 .. data address
# r0 .. crc
@micropython.asm_thumb
def _crc16_tr(r0, r1, r2, r3) -> uint:
    mov(r6, 0xff)
    label(loop)
    ldrb(r5, [r1, 0])  # idx = data[0]
    add(r1, 1)         # increment data pointer
    eor(r5, r0)        # idx ^= crc
    and_(r5, r6)       # idx ^= 0xff
    lsl(r5, r5, 1)     # double to make idx ptr16
    add(r5, r5, r3)    # table data address
    ldrh(r5, [r5, 0])  # fetch table entry: r5 = tab[idx]
    lsr(r0, r0, 8)     # crc >>= 8
    eor(r0, r5)        # crc ^= tab[idx]
    sub(r2, 1)         # n -= 1
    bne(loop)          # --- test and outer end ---

# --- internal ---
# r6 .. 0xff
# r5 .. idx or tab[idx]
# r4 .. working and test register
# --- arguments ---
# r3 .. lookup table address
# r2 .. n (length of data)
# r1 .. data address
# r0 .. crc
@micropython.asm_thumb
def _crc32_tr(r0, r1, r2, r3) -> uint:
    mov(r6, 0xff)
    label(loop)
    ldrb(r5, [r1, 0])  # idx = data[0]
    add(r1, 1)         # increment data pointer
    eor(r5, r0)        # idx ^= crc
    and_(r5, r6)       # idx ^= 0xff
    lsl(r5, r5, 2)     # * 4 to make idx ptr32            <-- difference for 32 vs 16 bit
    add(r5, r5, r3)    # table data address
    ldr(r5, [r5, 0])   # fetch table entry: r5 = tab[idx] <-- difference for 32 vs 16 bit
    lsr(r0, r0, 8)     # crc >>= 8
    eor(r0, r5)        # crc ^= tab[idx]
    sub(r2, 1)         # n -= 1
    bne(loop)          # --- test and outer end ---

# --- internal ---
# r7 .. working register
# r6 .. idx or tab[idx]
# r5 .. crc1
# r4 .. crc0
# --- arguments ---
# r3 .. lookup table address
# r2 .. n (length of data), used for the loop
# r1 .. data address
# r0 .. crc (ptr64), 0xff within loop
@micropython.asm_thumb
def _crc64_h(r0, r1, r2, r3):  # just a helper function
    ldr(r4, [r0, 0])        # crc0
    ldr(r5, [r0, 4])        # crc1, higher word of crc
    push({r0})
    mov(r0, 0xff)
    label(loop)
    ldrb(r6, [r1, 0])  # idx = data[0]
    add(r1, 1)         # increment data pointer
    eor(r6, r4)        # idx ^= crc0
    and_(r6, r0)       # idx ^= 0xff   # we can do this with 0xff immediate value !
    lsl(r6, r6, 3)     # to make idx ptr64
    add(r6, r6, r3)    # table data address
    lsl(r7, r5, 24)    # crc1 << 24
    lsr(r4, r4, 8)     # crc0 >> 8
    orr(r4, r7)        # crc1 << 24 | crc0 >> 8
    ldr(r7, [r6, 0])   # tab[idx]
    eor(r4, r7)        # (crc1 << 24 | crc0 >> 8) ^ tab[idx] , where tab..ptr64
    lsr(r5, r5, 8)     # crc1 >> 8
    ldr(r7, [r6, 4])   # tab[idx+1/2]   , where tab..ptr64
    eor(r5, r7)        # (crc1 >> 8) ^ tab[idx+1/2]
    sub(r2, 1)         # n -= 1
    bne(loop)          # --- test and outer end ---
    pop({r0})
    str(r4, [r0, 0])        # crc0
    str(r5, [r0, 4])        # crc1, higher word of crc

from array import array
acrc = array('Q', (0,))

def _crc64_tr(crc, data, n, tab):
    acrc[0] = crc
    _crc64_h(acrc, data, n, tab)
    return acrc[0]

import crc
crc.Implementation = 'asm_thumb'
crc._crc8_tr  = _crc8_tr
crc._crc16_tr = _crc16_tr
crc._crc32_tr = _crc32_tr
crc._crc64_tr = _crc64_tr