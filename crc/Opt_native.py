# Optimization import for Micropython crc class.
#
# 8-bit table based right shift native crc 8, 16 and 32 implementations

# --- arguments ---
# .. lookup table address
# .. n (length of data, will be ignored here)
# .. data to be processed, iterable of bytes
# .. crc
@micropython.native
def _crc8_tr(crc, data, n, tab):
    for d in data:
        crc = tab[crc ^ d]
    return crc

# --- arguments ---
# .. lookup table address
# .. n (length of data, will be ignored here)
# .. data to be processed, iterable of bytes
# .. crc
@micropython.native
def _crc16_tr(crc, data, n, tab):
    for d in data:
        crc = (crc >> 8) ^ tab[(crc ^ d) & 0xff]
    return crc

import crc
crc.Implementation = 'native'
crc._crc8_tr  = _crc8_tr
crc._crc16_tr = _crc16_tr
crc._crc32_tr = _crc16_tr
crc._crc64_tr = _crc16_tr