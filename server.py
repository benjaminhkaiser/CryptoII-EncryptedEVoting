import socket
from Crypto.PublicKey import RSA
from Crypto import Random

publicKeyFile = "serverpubkey.pem"

#writes public key to file, returns private key
def set_keys():
	rand = Random.new().read
	keys = RSA.generate(1024,rand)
	public_key = keys.publickey().exportKey()
	private_key = keys.exportKey(passphrase="cryptoII")

	pubHandle = open(publicKeyFile, 'w')
	pubHandle.write(public_key)
	
	return keys 

def listen_for_client():
	key = set_keys()	#generate keys
	s = socket.socket()	#create the socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345	#initialize the port to connect over
	s.bind((host, port))	#bind the socket to the port

	s.listen(5)	#listen for client connections
	while True:
		c, addr = s.accept()	#accept client connection
		votestring = str(addr) + " voted "	#add client address to string
		vote = c.recv(128)

		votestring += key.decrypt(vote)
		
		print votestring
		c.send("Vote registered.")	#send confirmation msg
		c.close()	#close client connection

if __name__ == "__main__":
	listen_for_client()			
