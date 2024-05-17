# Examples of the crc class

                                #  comment this out.    -- v -- v --  or replace with Opt_asm_xtensa,  Opt_viper !
from crc import Calculator, Crc8, Crc16, Crc32, Crc64, Opt_asm_thumb

data = bytes('123456789', 'utf-8')
data1 = bytes('123', 'utf-8')
data2 = bytes('456789', 'utf-8')

calculator = Calculator(Crc8.bluetooth)
print('Crc8.bluetooth:', hex(calculator.checksum(data)), 'Check:', hex(calculator.check))

calculator = Calculator(Crc16.profibus)
print('Crc16.profibus:', hex(calculator.checksum(data)))


config = {'width': 16,
          'poly':  0x1021,
          'init':  0x0000,
          'refin': False,
          'refout':False,
          'xorout':0xffff,
          'check': 0xce3c  # this is optional, try to comment it out
          }
calculator = Calculator(config)
#  ---  calculator.selftest_ok() is commented out in the crc.Calculator class  ---
# print('Crc selftest o.k.:', calculator.selftest_ok())
print('CRC:', hex(calculator.checksum(data)), 'Check:', hex(calculator.check))

calculator = Calculator(Crc32.autosar)
print('Crc32.autosar:', hex(calculator.checksum(data)), 'Check:', hex(calculator.check))

calculator = Calculator(Crc64.go_iso)
print('Crc64.go_iso:', hex(calculator.checksum(data)), 'Check:', hex(calculator.check))

calculator = Calculator(Crc16.usb)
calculator.digest(data1)
calculator.digest(data2)                         # We may digest first and then do a checksum.
print('Crc16.usb:', hex(calculator.checksum()), 'Check:', hex(calculator.check))         # The checksum resets the crc digestion.
calculator.digest(data1)
calculator.reset()
calculator.digest(data2)                         # We only digest the second data now
print('Crc16.usb:', hex(calculator.checksum()))  # The checksum is different now

crc_calc = Calculator(Crc8.crc7ls)           # crc7, result left shifted by 1 bit, as used in MM/SD cards
crc_calc.digest(data1)
crc = crc_calc.checksum(data2)               # We may digest first and then do a checksum.
print('Crc8.crc7ls:', hex(crc), 'Check:', hex(crc_calc.check))  # The checksum is different now


#  ---- Output here: -----
#
# Crc8.bluetooth: 0x26 Check: 0x26
# Crc16.profibus: 0xa819
# CRC: 0xce3c Check: 0xce3c
# Crc32.autosar: 0x1697d06a Check: 0x1697d06a
# Crc64.go_iso: 0xb90956c775a41001 Check: 0xb90956c775a41001
# Crc16.usb: 0xb4c8 Check: 0xb4c8
# Crc16.usb: 0x1a
# Crc8.crc7ls: 0xea Check: 0xea

