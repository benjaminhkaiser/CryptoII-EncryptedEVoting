#!/usr/bin/python

from charm.toolbox.integergroup import RSAGroup
from charm.schemes.pkenc import pkenc_paillier99  

group = RSAGroup()
pai = pkenc_paillier99.Pai99(group)
(public_key, secret_key) = pai.keygen()

msg1 = 1 
msg2 = 4 
msg3 = 4 
msg4 = 1 
msg5 = 16 
msg6 = 1 

msg1 = pai.encode(public_key['n'], msg1)
msg2 = pai.encode(public_key['n'], msg2)
msg3 = pai.encode(public_key['n'], msg3)
msg4 = pai.encode(public_key['n'], msg4)
msg5 = pai.encode(public_key['n'], msg5)
msg6 = pai.encode(public_key['n'], msg6)

ciphertext1 = pai.encrypt(public_key, msg1)
ciphertext2 = pai.encrypt(public_key, msg2)
ciphertext3 = pai.encrypt(public_key, msg3)
ciphertext4 = pai.encrypt(public_key, msg4)
ciphertext5 = pai.encrypt(public_key, msg5)
ciphertext6 = pai.encrypt(public_key, msg6)


ciphertext7 = ciphertext1 + ciphertext2 + ciphertext3 + ciphertext4 + ciphertext5 + ciphertext6

decrypt3 = pai.decrypt(public_key, secret_key, ciphertext7)

#convert int to string and grab k of k mod n
decrypt3 = str(decrypt3).partition('mod')[0]
decrypt3 = int(decrypt3)

print 'candidate 3:',decrypt3/16
decrypt3 = decrypt3 - 16*(decrypt3/16)

print 'candidate 2:',decrypt3/4
decrypt3 = decrypt3 - 4*(decrypt3/4)

print 'candidate 1:',decrypt3/1
