# Optimization import for Micropython crc class.
#
# 8-bit table based right shift asm_xtensa crc 8, 16 and 32 implementations

# --- internal ---
# a6 .. idx or tab[idx]
# --- arguments ---
# a5 .. lookup table address
# a4 .. n (length of data), then data address + n
# a3 .. data address
# a2 .. crc
@micropython.asm_xtensa
def _crc8_tr(a2, a3, a4, a5) -> uint:
    add(a4, a4, a3)    # final data address
    label(loop)
    l8ui(a6, a3, 0)    # a6 = idx = data[0]
    addi(a3, a3, 1)    # increment data pointer
    xor(a6, a6, a2)    # idx ^= crc
    add(a6, a6, a5)    # table data address
    l8ui(a2, a6, 0)    # fetch table entry: a2 = tab[idx]
    bne(a3, a4, loop)  # --- test and outer end ---

# --- internal ---
# a7 .. 0xff
# a6 .. idx or tab[idx]
# --- arguments ---
# a5 .. lookup table address
# a4 .. n (length of data), then data address + n
# a3 .. data address
# a2 .. crc
@micropython.asm_xtensa
def _crc16_tr(a2, a3, a4, a5) -> uint:
    movi(a7, 0xff)
    add(a4, a4, a3)    # final data address
    label(loop)
    l8ui(a6, a3, 0)    # a6 = idx = data[0]
    addi(a3, a3, 1)    # increment data pointer
    xor(a6, a6, a2)    # idx ^= crc
    and_(a6, a6, a7)   # idx &= 0xff
    data(3, 0x110000 | 6<<12 | 6<<8 | (16-1)<<4)  # a6 <<= 1, double to make idx ptr16
    add(a6, a6, a5)    # table data address
    l16ui(a6, a6, 0)   # fetch table entry: a6 = tab[idx]
    data(3, 0x410000 | 2<<12 | 2<<4 | 8<<8)
    xor(a2, a2, a6)    # crc ^= tab[idx]
    bne(a3, a4, loop)  # --- test and outer end ---

# --- internal ---
# a7 .. 0xff
# a6 .. idx or tab[idx]
# --- arguments ---
# a5 .. lookup table address
# a4 .. n (length of data), then data address + n
# a3 .. data address
# a2 .. crc
@micropython.asm_xtensa
def _crc32_tr(a2, a3, a4, a5) -> uint:
    movi(a7, 0xff)
    add(a4, a4, a3)    # final data address
    label(loop)
    l8ui(a6, a3, 0)    # a6 = idx = data[0]
    addi(a3, a3, 1)    # increment data pointer
    xor(a6, a6, a2)    # idx ^= crc
    and_(a6, a6, a7)   # idx &= 0xff
    data(3, 0x110000 | 6<<12 | 6<<8 | (16-2)<<4) # slli(a6, a6, 2)  # a6 <<= 2  #  idx *= 4 to make idx ptr32
    add(a6, a6, a5)    # table data address
    l32i(a6, a6, 0)    # fetch table entry: a6 = tab[idx]
    data(3, 0x410000 | 2<<12 | 2<<4 | 8<<8)     # srli(a2, a2, 8)   # a2 >>= 8  # crc >>= 8
    xor(a2, a2, a6)    # crc ^= tab[idx]
    bne(a3, a4, loop)  # --- test and outer end ---

# --- internal ---   # a2..a7, a12..a15 avail.
# a14 .. 0xff
# a13 .. working register
# a12 .. idx or tab[idx]   
# a7 .. crc1
# a6 .. crc0
# --- arguments ---
# a5 .. lookup table address
# a4 .. n (length of data), then data address + n
# a3 .. data address
# a2 .. crc (ptr64), 0xff within loop
@micropython.asm_xtensa
def _crc64_h(a2, a3, a4, a5):
    l32i(a6, a2, 0)        # crc0
    l32i(a7, a2, 4)        # crc1, higher word of crc
    movi(a14, 0xff)
    add(a4, a4, a3)        # final data address
    label(loop)        # ----- loop start
    l8ui(a12, a3, 0)       # a12 = idx = data[0]
    addi(a3, a3, 1)        # increment data pointer
    xor(a12, a12, a6)      # idx ^= crc0
    and_(a12, a12, a14)    # idx &= 0xff
    data(3, 0x110000 | 12<<12 | 12<<8 | (16-3)<<4) # slli(a12, a12, 3)  # a12 <<= 3  # make idx ptr64
    add(a12, a12, a5)      # table data address now in a12 
    data(3, 0x010000 | 13<<12 | 7<<8 | (32-24)<<4)  # slli(a13, a7, 24)         # crc1 << 24
    data(3, 0x410000 | 6<<12 | 6<<4 | 8<<8)     # srli(a6, a6, 8)   # a6 >>= 8  # crc0 >> 8
    or_(a6, a6, a13)                                                            # crc1 << 24 | crc0 >> 8
    l32i(a13, a12, 0)                                                           # a13 = tab[idx]
    xor(a6, a6, a13)       # crc0 = (crc1 << 24 | crc0 >> 8) ^ tab[idx] , where tab..ptr64
    data(3, 0x410000 | 7<<12 | 7<<4 | 8<<8)     # srli(a7, a7, 8)   # a7 >>= 8  # crc1 >>= 8
    l32i(a13, a12, 4)                           # tab[idx+1/2]   , where tab..ptr64    
    xor(a7, a7, a13)       # crc1 = (crc1 >> 8) ^ tab[idx+1/2]
    bne(a3, a4, loop)  # --- test and outer end ---
    s32i(a6, a2, 0)        # crc0
    s32i(a7, a2, 4)        # crc1, higher word of crc


from array import array
acrc = array('Q', (0,))

def _crc64_tr(crc, data, n, tab):
    acrc[0] = crc
    _crc64_h(acrc, data, n, tab)
    return acrc[0]

import crc
crc.Implementation = 'asm_xtensa'
crc._crc8_tr  = _crc8_tr
crc._crc16_tr = _crc16_tr
crc._crc32_tr = _crc32_tr
crc._crc64_tr = _crc64_tr