# -*- coding: utf-8 -*-
# created by: Gerardo Rivera López
# Implementation of primitive encryption algorithms
# released under the GNU GPL v2 license
# 
# github.com/gearlo


class cipher:
    def __init__(self, key):
        self.key = key
    def encrypt(file_block):
        pass
    def decrypt(self,file_block):
        pass



alphabet = ['a','b','c','d','e','f','g','h','i','j',
            'k','l','m','n','o','p','q','r','s','t',
            'u','v','w','x','y','z','A','B','C','D',
            'E','F','G','H','I','J','K','L','M','N',
            'O','P','Q','R','S','T','U','V','W','X',
            'Y','Z','0','1','2','3','4','5','6','7',
            '8','9']

alphabet2 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F',
            'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
            'W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','_','-']

class vigenereCipher(cipher):
    def __init__(self, key):
        self.key = []
        for k in key:
            if k in alphabet:
                self.key.append( alphabet.index(k) )
        #print self.key
    def encrypt(self,file_block):
        data_out = '' ; i = 0
        for p in file_block:
            if p in alphabet:
                data_out = data_out + alphabet[ (alphabet.index(p) +  self.key[i % len(self.key)]) % len(alphabet)]
                i = i + 1
            else:
                data_out = data_out + p
        return data_out
    def decrypt(self,file_block):
        data_out = ''; i = 0
        for c in file_block:
            if c in alphabet:
                data_out = data_out + alphabet[ (alphabet.index(c) -  self.key[i % len(self.key)]) % len(alphabet)]
                i = i + 1
            else:
                data_out = data_out + c
        return data_out


class caesarCipher(cipher):

    def __init__(self, key):
        self.encry = vigenereCipher('d')

    def encrypt(self,file_block):
        return self.encry.encrypt(file_block)

    def decrypt(self, file_block):
        return self.encry.decrypt(file_block)


class monoAlphabeticCipher(cipher):

    def __init__(self, key):
        self.encry = vigenereCipher(key[0])

    def encrypt(self,file_block):
        return self.encry.encrypt(file_block)

    def decrypt(self, file_block):
        return self.encry.decrypt(file_block)




from binascii import hexlify
from binascii import unhexlify
class vernanCipher(cipher):
    def __init__(self, key):
        self.key = []
        for k in key:
            self.key.append( int(hexlify(k),16) )
        #print self.key
    def __XOR(self, data_block):
        data_out = ''; i = 0
        for p in data_block:
            data_out = data_out + unhexlify(hex(int(hexlify(p),16) ^ self.key[i % len(self.key)])[2:].zfill(2))
            i = i + 1
        return data_out
    def encrypt(self, data_block):
        return self.__XOR(data_block)
    def decrypt(self,data_block):
        return self.__XOR(data_block)


from hashlib import md5
class infiniteKey:
    def __init__(self, key):
        self.key = []
        self.getsNumber = 0
        for char in key:
            self.key.append( int(hexlify(char),16) )

    def getKey(self):
        self.getsNumber = self.getsNumber + 1
        average = 0
        for l in self.key:
            average = average + l

        average = average / len(self.key)

        i = 0; new_string = ''
        while(i < len(self.key)):
            self.key[i] = self.key[i] + (self.key[i] % average)
            new_string = new_string + alphabet[self.key[i] % len(alphabet)]
            i = i + 1

        return str(md5(new_string + str(self.getsNumber)).hexdigest())


from math import ceil
class oneTimePad(cipher):
    def __init__(self, key):
        self.keyGen = infiniteKey(key)

    def __iXOR(self, data_block):
        key = ''; j = 0
        while(j < ceil(len(data_block)/32.0)):
            key = key + self.keyGen.getKey()
            j = j + 1

        data_out = ''; i = 0
        for p in data_block:
            data_out = data_out + unhexlify(hex(int(  hexlify(p),16) ^  int(key[i],16) )[2:].zfill(2))
            i = i + 1
        return data_out

    def encrypt(self, data_block):
        return self.__iXOR(data_block)
    def decrypt(self,data_block):
        return self.__iXOR(data_block)




import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def checksum(f_in):
    with open(f_in, 'rb') as fh:
        m = md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def reduceMd5(md5):
    result = ''
    i = 0
    while i < len(md5):
        hex = md5[i: i +3]
        dec = int(hex, 16)
        result = result + alphabet[ dec/ len(alphabet) ] + alphabet[ dec%len(alphabet) ]
        i = i + 3
        
    return result