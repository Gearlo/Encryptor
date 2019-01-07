# -*- coding: utf-8 -*-
# created by: Gerardo Rivera López
# released under the GNU GPL v2 license
# 
# github.com/gearlo

from techniques import monoAlphabeticCipher, 
                       vigenereCipher, 
                       vernanCipher, 
                       oneTimePad, 
                       AESCipher as AES, 
                       checksum

from binascii import unhexlify



def encrypt(file_in, key, techniques):
    blockSize = 4096
    T = []
    T.append( monoAlphabeticCipher()    ) #caesar Cipher
    T.append( monoAlphabeticCipher(key) )
    T.append( vigenereCipher(key)       )
    T.append( vernanCipher(key)         )
    T.append( oneTimePad(key)           )

    f_in = open(file_in,'rb')
    f_out = open(file_in + '.cry', 'wb')
    f_out.write('CRYOGENESIS' + unhexlify('00') + 'ARCHIVE' + unhexlify('01'))

    t_list = ''
    for t in techniques:
        t_list = t_list + str(t) + ':'

    file_header =  '|header|' + f_in.name + '|'+ t_list +'|' + checksum(file_in)
    aes = AES(key)
    f_out.write( aes.encrypt(file_header) )
    f_out.write( unhexlify('02') )

    block = f_in.read(blockSize)
    while(block):
        block_c = block
        for t in techniques:
            block_c = T[t].encrypt(block_c)
        f_out.write(block_c)
        block = f_in.read(blockSize)


    f_in.close()
    f_out.close()


def decrypt(file_in, key):
    blockSize = 4096
    T = []
    T.append( monoAlphabeticCipher()    ) #caesar Cipher
    T.append( monoAlphabeticCipher(key) )
    T.append( vigenereCipher(key)       )
    T.append( vernanCipher(key)         )
    T.append( oneTimePad(key)           )

    f_in = open(file_in,'rb'); header = ''

    if(f_in.read(20) == ('CRYOGENESIS' + unhexlify('00') + 'ARCHIVE' + unhexlify('01'))):
        while(True):
            c = f_in.read(1)
            if c == unhexlify('02'):
                break
            else:
                header = header + c
    else:
        print 'this is not an encrypted file'
    #header

    aes = AES(key)
    header_sections = aes.decrypt(header).split('|')
    #print header_sections
    if header_sections[1] != 'header':
        print 'Incorrect password'
        from sys import exit; exit(0)

    techniques = []
    for t in header_sections[3].split(':'):
        if(t != ''):
            techniques.append(int(t))

    techniques.reverse()
    f_out = open(header_sections[2] + '.out','wb')
    block = f_in.read(blockSize)
    while(block):
        for t in techniques:
            block = T[t].decrypt(block)
        f_out.write(block)
        block = f_in.read(blockSize)

    f_out.close()
    f_in.close()

    if(checksum(header_sections[2] + '.out') != header_sections[4]):
        print 'the encrypted file is corrupted'
        from os import remove ; remove(header_sections[2] + '.out')
