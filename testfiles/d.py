#!/usr/bin/python
import socket
import hashlib

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Random.random import getrandbits
import registrar
import sys


from charm.toolbox.integergroup import RSAGroup
from charm.schemes.pkenc import pkenc_paillier99
from charm.toolbox.conversion import Conversion
from charm.core.math import integer as specialInt
from charm.toolbox.integergroup import integer

import charm
from charm.core.engine.util import objectToBytes,bytesToObject

def get_vote():
	vote = 2

        group = RSAGroup()
        pai = pkenc_paillier99.Pai99(group)

        f=open('./pyssss/VotingPublic','rb')
        data = f.read()
        public_key = bytesToObject(data,group)

        vote = pai.encode(public_key['n'],vote)
        ciphervote = pai.encrypt(public_key,vote)
        print ciphervote['c']
	ciphertext= specialInt.serialize(ciphervote['c'])
	print ciphertext	
#	ciphervote['c'] = Conversion.bytes2integer(Conversion.IP2OS(7092577248503691820499926901328776752053429606540181306976))

        f=open('./pyssss/VotingPrivate','rb')
        data = f.read()
        secret_key = bytesToObject(data,group)
	ciphertext = specialInt.deserialize(ciphertext)
        #plaintext=pai.decrypt(public_key, secret_key,ciphervote)
	n, n2 = public_key['n'], public_key['n2']
       	plaintext = ((pai.L(ciphertext ** secret_key['lamda'],n) % n) * secret_key['u']) %n 

	print plaintext










        ciphervote=42
        return ciphervote

if __name__ == "__main__":
        get_vote()

