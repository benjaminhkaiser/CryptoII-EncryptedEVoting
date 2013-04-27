import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

publicKeyFile = "serverpubkey.pem"

#writes public key to file, returns private key
def set_RSA_keys():
	#generate random number, then keys
	rand = Random.new().read
	keys = RSA.generate(1024,rand)

	#write public key to file
	public_key = keys.publickey().exportKey()
	pubHandle = open(publicKeyFile, 'w')
	pubHandle.write(public_key)
	
	return keys 

def listen_for_client():
	key = set_RSA_keys()	#generate RSA keys
	s = socket.socket()	#create the socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345	#initialize the port to connect over
	s.bind((host, port))	#bind the socket to the port

	s.listen(5)	#listen for client connections
	while True:
		c, addr = s.accept()	#accept client connection
		
		#get AES info and decrypt using RSA private key
		AES_key = key.decrypt(c.recv(128))
		AES_iv = key.decrypt(c.recv(128))
		
		#get vote encrypted by AES and decrypt
		AES_decryptor = AES.new(AES_key, AES.MODE_CBC, AES_iv)
		vote = c.recv(128)
		vote = AES_decryptor.decrypt(vote)

		print (str(addr) + " voted " + vote)
		
		c.send("Vote registered.")	#send confirmation msg
		c.close()	#close client connection

if __name__ == "__main__":
	listen_for_client()			
