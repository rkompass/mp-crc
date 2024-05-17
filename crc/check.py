# Do a check for correctness of all available CRC algorithms



from crc import Calculator, Crc8, Crc16, Crc32, Crc64, Opt_asm_thumb

data = bytes('123456789', 'utf-8')
data1 = bytes('123', 'utf-8')
data2 = bytes('456789', 'utf-8')

for crcgrp in (Crc8, Crc16, Crc32, Crc64):
    grpname = getattr(crcgrp, '__name__')
    for alg in dir(crcgrp):
        if not alg.startswith('__'):
            crcfun = Calculator(getattr(crcgrp, alg))
            crcfun.digest(data1)
            crc = crcfun.checksum(data2)
            chk_ok = crc == crcfun.check
            # print(f'Algorithm: {grpname+'.'+alg:15s} CRC("123456789") = 0x{crc:x}.   Check: {'O.K.' if chk_ok else 'Wrong'}')
            print('Algorithm: ', grpname+'.'+alg,' CRC("123456789") = 0x',crc,'.   Check: ','O.K.' if chk_ok else 'Wrong')
        
        
