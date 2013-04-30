import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import sys

from charm.core.math import integer as specialInt
from charm.toolbox.integergroup import RSAGroup
from charm.schemes.pkenc import pkenc_paillier99
from charm.core.engine.util import objectToBytes,bytesToObject
from charm.schemes.pkenc.pkenc_paillier99 import Ciphertext
publicKeyFile = "serverpubkey.pem"
ciphervotesFile = "CipherVotes"
ciphervotesTotalFile = "CipherVotesTotal"

numvoters = 3
voteSize=128
signedVoteSize=320
serverPublicKeySize = 1024
#writes public key to file, returns private key
def set_RSA_keys(): 
	#generate random number, then keys
	rand = Random.new().read
	keys = RSA.generate(serverPublicKeySize,rand)

	#write public key to file
	public_key = keys.publickey().exportKey()
	pubHandle = open(publicKeyFile, 'w')
	pubHandle.write(public_key)
	
	return keys 

def listen_for_client():
	key = set_RSA_keys()	#generate RSA keys
	s = socket.socket()	#create the socket
	host = socket.gethostname()	#get the host name of the socket
	port = (int(sys.argv[1]))	#initialize the port to connect over
	s.bind((host, port))	#bind the socket to the port

	s.listen(5)	#listen for client connections

	
	#initialize 
	group = RSAGroup()
	pai = pkenc_paillier99.Pai99(group)
	
	#get voting public key	
	f=open('./pyssss/VotingPublic','rb')
	data=f.read()
	public_key=bytesToObject(data,group)	
	
	#count variable for initial ciphervotetotal
	count = 0
	while True:
		c, addr = s.accept()	#accept client connection
		
		#get AES info and decrypt using RSA private key
		AES_key = key.decrypt(c.recv(128))
		AES_iv = key.decrypt(c.recv(128))
		
		#get vote and signed vote, decrypt, unpad
		AES_decryptor = AES.new(AES_key, AES.MODE_CBC, AES_iv)
		vote = c.recv(voteSize)
		signed_vote = c.recv(signedVoteSize)
		vote = AES_decryptor.decrypt(vote)
		signed_vote = [long(AES_decryptor.decrypt(signed_vote).strip()),None]
		
		#load notary public key
		f = open("NotaryKey.pem",'r')
		not_pub_key = RSA.importKey(f.read())
		f.close()
	
		#use notary public key to verify signed vote against regular vote
		print("Verification: ", not_pub_key.verify(vote, signed_vote))

		#write votes to file in serialized format to be opened later	
		f=open(ciphervotesFile,'a')
		f.write(vote)
		f.write('\n')
		
		#deserialize vote 
		ciphervote = specialInt.deserialize(vote)
		ciphervote = Ciphertext({'c':ciphervote},public_key,'c')

		#homomorphically add votes
		if count == 0:
			ciphervotestotal = ciphervote
		else:		
			ciphervotestotal = ciphervotestotal + ciphervote
	
		#print (str(addr) + " voted " + vote)
		

		c.send("Vote registered.")	#send confirmation msg
		c.close()	#close client connection
		
		count = count + 1

		if count == numvoters:
			#write total vote to file in serizlied format to be opened later
			f=open(ciphervotesTotalFile,'wb')
			f.write(specialInt.serialize(ciphervotestotal['c']))
			break


if __name__ == "__main__":
	listen_for_client()			
	
	



