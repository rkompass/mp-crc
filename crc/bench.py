# Benchmark of the crc class
import gc
gc.collect(); free= gc.mem_free(); print('Free:', free, 'bytes.')
from time import ticks_us, ticks_diff           # v-- one of Opt_native, Opt_viper, Opt_asm_xtensa, Opt_asm_thumb
from crc import Calculator, Crc8, Crc16, Crc32, Crc64, Opt_asm_thumb   # or comment the Opt out
gc.collect(); free= gc.mem_free(); print('Free:', free, 'bytes.')

data = bytearray((i%256 for i in range(10_000)))

crc8 = Calculator(Crc8.maxim_dow)
print('Crc implementation:', crc8.implementation)
for i in range(3):
    t0 = ticks_us()
    crc8.digest(data)
    crc = crc8.checksum()
    t1 = ticks_us()
    td = ticks_diff(t1,t0)
    print(f'crc8: 0x{crc:02x}, {td/len(data):6.2f}µs per byte')

crc16 = Calculator(Crc16.ccitt)
for i in range(3):
    t0 = ticks_us()
    crc16.digest(data)
    crc = crc16.checksum()
    t1 = ticks_us()
    td = ticks_diff(t1,t0)
    print(f'crc16: 0x{crc:04x}, {td/len(data):6.2f}µs per byte')

crc32 = Calculator(Crc32.crc32)
for i in range(3):
    t0 = ticks_us()
    crc32.digest(data)
    crc = crc32.checksum()
    t1 = ticks_us()
    td = ticks_diff(t1,t0)
    print(f'crc32: 0x{crc:08x}, {td/len(data):6.2f}µs per byte')

# builtin crc32 from binascii
import binascii
for i in range(3):
    t0 = ticks_us()
    crc = binascii.crc32(data)
    t1 = ticks_us()
    td = ticks_diff(t1,t0)
    print(f'binascii.crc32: 0x{crc:08x}, {td/len(data):6.2f}µs per byte')

crc64 = Calculator(Crc64.crc64)
for i in range(3):
    t0 = ticks_us()
    crc64.digest(data)
    crc = crc64.checksum()
    t1 = ticks_us()
    td = ticks_diff(t1,t0)
    print(f'crc64: 0x{crc:08x}, {td/len(data):6.2f}µs per byte')


# Blackpill STM32F411 @ 96MHz

# Crc implementation: bytecode
# crc8: 0x0c,   9.02µs per byte
# crc8: 0x0c,   9.02µs per byte
# crc8: 0x0c,   9.02µs per byte
# crc16: 0x3359,  12.65µs per byte
# crc16: 0x3359,  12.65µs per byte
# crc16: 0x3359,  12.65µs per byte
# crc32: 0xd6bbe339,  72.72µs per byte
# crc32: 0xd6bbe339,  72.89µs per byte
# crc32: 0xd6bbe339,  72.88µs per byte
# crc64: 0xcca94235057ad7ea,  76.10µs per byte
# crc64: 0xcca94235057ad7ea,  76.36µs per byte
# crc64: 0xcca94235057ad7ea,  76.27µs per byte

# Crc implementation: viper
# crc8: 0x0c,   0.46µs per byte
# crc8: 0x0c,   0.46µs per byte
# crc8: 0x0c,   0.46µs per byte
# crc16: 0x3359,   0.63µs per byte
# crc16: 0x3359,   0.63µs per byte
# crc16: 0x3359,   0.63µs per byte
# crc32: 0xd6bbe339,   0.68µs per byte
# crc32: 0xd6bbe339,   0.67µs per byte
# crc32: 0xd6bbe339,   0.67µs per byte
# crc64: 0xcca94235057ad7ea,   1.33µs per byte
# crc64: 0xcca94235057ad7ea,   1.32µs per byte
# crc64: 0xcca94235057ad7ea,   1.32µs per byte

# Crc implementation: asm_thumb
# crc8: 0x0c,   0.13µs per byte
# crc8: 0x0c,   0.13µs per byte
# crc8: 0x0c,   0.13µs per byte
# crc16: 0x3359,   0.18µs per byte
# crc16: 0x3359,   0.17µs per byte
# crc16: 0x3359,   0.18µs per byte
# crc32: 0xd6bbe339,   0.20µs per byte
# crc32: 0xd6bbe339,   0.19µs per byte
# crc32: 0xd6bbe339,   0.19µs per byte
# crc64: 0xcca94235057ad7ea,   0.26µs per byte
# crc64: 0xcca94235057ad7ea,   0.26µs per byte
# crc64: 0xcca94235057ad7ea,   0.26µs per byte

