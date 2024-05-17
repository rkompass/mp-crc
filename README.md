# mp-crc

This is an accelerated table-based crc library for micropython that implements a variety of crc variants from 8 to 64 bits.
Crc variants may be added by uncommenting or adding their definitions in `crc/init.py` or be defined in a dict (see below).

At present these definitions are active:
```py
class Crc8:
    # Name      (Width, Poly, Init, RefIn, RefOut, Xorout, Check)
    crc7ls    = (8,     0x12, 0x00, False, False,  0x00,   0xea)
    crc8      = (8,     0x07, 0x00, False, False,  0x00,   0xf4)
    ccitt     = crc8
    saej1850  = (8,     0x1d, 0x00, False, False,  0x00,   0x37)
    autosar   = (8,     0x2f, 0xff, False, False,  0xff,   0xdf)
    bluetooth = (8,     0xa7, 0x00, True,  True,   0x00,   0x26)
    maxim_dow = (8,     0x31, 0x00, True,  True,   0x00,   0xa1)
#     cdma2000  = (8,     0x9b, 0xff, False, False,  0x00,   0xda)
#     darc      = (8,     0x39, 0x00, True,  True,   0x00,   0x15)
#     dvb_s2    = (8,     0xd5, 0x00, False, False,  0x00,   0xbc)
#     ebu       = (8,     0x1d, 0xff, True,  True,   0x00,   0x97)
#     i_code    = (8,     0x1d, 0xfd, False, False,  0x00,   0x7e)
#     itu       = (8,     0x07, 0x00, False, False,  0x55,   0xa1)
#     rohc      = (8,     0x07, 0xff, True,  True,   0x00,   0xd0)
#     wcdma     = (8,     0x9b, 0x00, True,  True,   0x00,   0x25)

class Crc16:
    # Name      (Width,  Poly,   Init,   RefIn, RefOut, Xorout, Check)
    xmodem    = (16,    0x1021, 0x0000, False, False,  0x0000, 0x31c3)
    usb       = (16,    0x8005, 0xffff, True,  True,   0xffff, 0xb4c8)
    ccitt     = xmodem
    gsm       = (16,    0x1021, 0x0000, False, False,  0xffff, 0xce3c)
    profibus  = (16,    0x1dcf, 0xffff, False, False,  0xffff, 0xa819)
    modbus    = (16,    0x8005, 0xffff, True,  True,   0x0000, 0x4b37)
#     arc       = (16,    0x8005, 0x0000, True,  True,   0x0000, 0xbb3d),
#     buypass   = (16,    0x8005, 0x0000, False, False,  0x0000, 0xfee8),
#     dds_110   = (16,    0x8005, 0x800d, False, False,  0x0000, 0x9ecf),
#     maxim     = (16,    0x8005, 0x0000, True,  True,   0xffff, 0x44c2),
#     aug_ccitt = (16,    0x1021, 0x1d0f, False, False,  0x0000, 0xe5cc),
#     ccitt_false=(16,    0x1021, 0xffff, False, False,  0x0000, 0x29b1),
#     genibus   = (16,    0x1021, 0xffff, False, False,  0xffff, 0xd64e),
#     kermit    = (16,    0x1021, 0x0000, True,  True,   0x0000, 0x2189),
#     mcrf4xx   = (16,    0x1021, 0xffff, True,  True,   0x0000, 0x6f91),
#     riello    = (16,    0x1021, 0xb2aa, True,  True,   0x0000, 0x63d0),
#     tms37157  = (16,    0x1021, 0x89ec, True,  True,   0x0000, 0x26b1),
#     x_25        (16,    0x1021, 0xffff, True,  True,   0xffff, 0x906e),
#     a           (16,    0x1021, 0xc6c6, True,  True,   0x0000, 0xbf05)
#     cdma2000  = (16,    0xc867, 0xffff, False, False,  0x0000, 0x4c06),
#     dect_r    = (16,    0x0589, 0x0000, False, False,  0x0001, 0x007e),
#     dect_x    = (16,    0x0589, 0x0000, False, False,  0x0000, 0x007f),
#     dnp       = (16,    0x3d65, 0x0000, True,  True,   0xffff, 0xea82),
#     en_13757  = (16,    0x3d65, 0x0000, False, False,  0xffff, 0xc2b7),
#     t10-dif   = (16,    0x8bb7, 0x0000, False, False,  0x0000, 0xd0db),
#     teledisk  = (16,    0xa097, 0x0000, False, False,  0x0000, 0x0fb3),

class Crc32:
    # Name     (Width,  Poly,       Init,       RefIn, RefOut, Xorout,     Check)
    crc32      = (32,    0x04c11db7, 0xffffffff, True,  True,   0xffffffff, 0xcbf43926)
    autosar    = (32,    0xf4acfb13, 0xffffffff, True,  True,   0xffffffff, 0x1697d06a)
    bzip2      = (32,    0x04c11db7, 0xffffffff, False, False,  0xffffffff, 0xfc891918)
    posix      = (32,    0x04c11db7, 0x00000000, False, False,  0xffffffff, 0x765e7680)
    sata       = (32,    0x04c11db7, 0x52325032, False, False,  0x00000000, 0xcf72afe8)
#     jamcrc     = (32,    0x04c11db7, 0xffffffff, True,  True,   0x00000000, 0x340bc6d9)
#     mpeg-2     = (32,    0x04c11db7, 0xffffffff, False, False,  0x00000000, 0x0376e6e7)
#     xfer       = (32,    0x000000af, 0x00000000, False, False,  0x00000000, 0xbd0be338)
#     c          = (32,    0x1edc6f41, 0xffffffff, True,  True,   0xffffffff, 0xe3069283)
#     d          = (32,    0xa833982b, 0xffffffff, True,  True,   0xffffffff, 0x87315576)
#     q          = (32,    0x814141ab, 0x00000000, False, False,  0x00000000, 0x3010bf7f)
    
class Crc64:
    # Name   (Width,  Poly,           Init,                RefIn, RefOut, Xorout,             Check)
    crc64   = (64, 0x42f0e1eba9ea3693, 0x0000000000000000, False, False,  0x0000000000000000, 0x6c40df5f0b497347)
    ecma_182 = crc64
    go_iso  = (64, 0x000000000000001b, 0xffffffffffffffff, True,  True,   0xffffffffffffffff, 0xb90956c775a41001)
#     we      = (64, 0x42f0e1eba9ea3693, 0xffffffffffffffff, False, False,  0xffffffffffffffff, 0x62ec59e3f1a4f00a)
#     xz      = (64, 0x42f0e1eba9ea3693, 0xffffffffffffffff, True,  True,   0xffffffffffffffff, 0x995dc9bbdf1939fa)
```

Implementations of the crc calculations are available as ordinary MP (interpreted bytecode), native, viper, asm_xtensa or asm_thumb.

For using a certain crc variant (e.g. crc16 ccitt) and acceleration (e.g. asm_thumb) you import like:
```py
from crc import Calculator, Crc16, Opt_asm_thumb
```
Which imports the main Calculator class, the Crc16 definitions (which include ccitt) and (optionally) the optimized asm_thumb implementation.

Then you create the actual calculator (which includes a computation of the look-up table) by:
```py
calculator = Calculator(Crc16.ccitt)
```

You may then use it to calculate and return the crc with e.g.:
```py
data = bytes('123456789', 'utf-8')
print('Crc16.ccitt:', hex(calculator.checksum(data)))
```

Often you do not want to return the crc computation result directly but digest a lot of data first.
For that there is a `.digest()` member function:
```py
data1 = bytes('123', 'utf-8')
data2 = bytes('456789', 'utf-8')

calculator.digest(data1)
calculator.digest(data2)                         # We may digest first and then do a checksum.
print('Crc16.usb:', hex(calculator.checksum())
```

Note that the `.checksum()` member function also does a reset of the internal crc computation state.

Crc definition may be defined on-the-fly like:
```py
config = {'width': 16,
          'poly':  0x1021,
          'init':  0x0000,
          'refin': False,
          'refout':False,
          'xorout':0xffff,
          'check': 0xce3c  # this is optional, may comment it out
          }
calculator = Calculator(config)
```

The file `examples.py`contains more usage examples. I recommend studying it.
The file `check.py` contains a checksum test for the present crc definitions.
The file `bench.py` does a benchmark of the crc computations.

Example benchmark results:
```txt
Blackpill STM32F411 @ 96MHz

Crc implementation: bytecode
crc8: 0x0c,   9.02µs per byte
crc8: 0x0c,   9.02µs per byte
crc8: 0x0c,   9.02µs per byte
crc16: 0x3359,  12.65µs per byte
crc16: 0x3359,  12.65µs per byte
crc16: 0x3359,  12.65µs per byte
crc32: 0xd6bbe339,  72.72µs per byte
crc32: 0xd6bbe339,  72.89µs per byte
crc32: 0xd6bbe339,  72.88µs per byte
crc64: 0xcca94235057ad7ea,  76.10µs per byte
crc64: 0xcca94235057ad7ea,  76.36µs per byte
crc64: 0xcca94235057ad7ea,  76.27µs per byte

Crc implementation: viper
crc8: 0x0c,   0.46µs per byte
crc8: 0x0c,   0.46µs per byte
crc8: 0x0c,   0.46µs per byte
crc16: 0x3359,   0.63µs per byte
crc16: 0x3359,   0.63µs per byte
crc16: 0x3359,   0.63µs per byte
crc32: 0xd6bbe339,   0.68µs per byte
crc32: 0xd6bbe339,   0.67µs per byte
crc32: 0xd6bbe339,   0.67µs per byte
crc64: 0xcca94235057ad7ea,   1.33µs per byte
crc64: 0xcca94235057ad7ea,   1.32µs per byte
crc64: 0xcca94235057ad7ea,   1.32µs per byte

Crc implementation: asm_thumb
crc8: 0x0c,   0.13µs per byte
crc8: 0x0c,   0.13µs per byte
crc8: 0x0c,   0.13µs per byte
crc16: 0x3359,   0.18µs per byte
crc16: 0x3359,   0.17µs per byte
crc16: 0x3359,   0.18µs per byte
crc32: 0xd6bbe339,   0.20µs per byte
crc32: 0xd6bbe339,   0.19µs per byte
crc32: 0xd6bbe339,   0.19µs per byte
crc64: 0xcca94235057ad7ea,   0.26µs per byte
crc64: 0xcca94235057ad7ea,   0.26µs per byte
crc64: 0xcca94235057ad7ea,   0.26µs per byte
```

The file `Opt_asm_xtensa.py` is an example of using the `@micropython.asm_xtensa` decorator. Which seems to be only a partial implementation.
The limitations may be overcome by using the `data()`statement.
I created preliminary docs for it and presented them [here](https://github.com/orgs/micropython/discussions/12965).
Using it enables fast calculations for the esp8266 architecture.
Unfortunately for the esp32 the `@micropython.asm_xtensawin` decorator would be needed, which is not available.
So you are limited to viper if you want to do fast calculations (without resorting to C) on esp32.

