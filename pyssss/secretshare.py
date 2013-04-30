#!/usr/bin/python
import random

from GF256elt import GF256elt
from PGF256 import PGF256
from PGF256Interpolator import PGF256Interpolator
from PySSSS import * 
import StringIO

from charm.toolbox.integergroup import RSAGroup 
from charm.schemes.pkenc import pkenc_paillier99
from charm.core.engine.util import objectToBytes,bytesToObject
from optparse import OptionParser

n=5
k=3
prefix="VotingSharedSecret"
usage="You can generate secrets or combine sercrets,n=5,k=3"
parser = OptionParser(usage=usage)

parser.add_option("-g","--generate-secrets",action="store_true",dest="generate",default=False)
parser.add_option("-c","--combine-secrets",action="store_true",dest="combine",default=False)

(options, args) = parser.parse_args()

if(options.generate == False and options.combine == False):
	print parser.print_help() 


if(options.generate):
	outputs=[]
	group = RSAGroup()
	pai = pkenc_paillier99.Pai99(group)
	(public_key, secret_key) = pai.keygen(secparam=16)

	#sharedsecret = str(secret_key['u']) + ',' + str(secret_key['lamda'])
#	sharedsecret = "message"
	sharedsecret = objectToBytes(secret_key,group)
	print sharedsecret
	input = StringIO.StringIO(sharedsecret)


	for i in xrange(n):
		outputs.append(StringIO.StringIO())

	encode(input,outputs,k)


	for i in xrange(n):
#		print outputs[i].getvalue().encode('hex')
		f = open(prefix+str(i),'w')
		f.write(outputs[i].getvalue())

	f=open("VotingPublic",'wb')
	f.write(objectToBytes(public_key,group))

	#f=open("VotingPrivate",'wb')
	#f.write(objectToBytes(secret_key,group))

	print "Public key n,g,n**2 placed into file VotingPublic"
	print "Shared secret key u,lambda placed into files VotingSharedSecret0 - VotingSharedSecretN"

if(options.combine):
		
	inputs = []
	for i in xrange(k):
		
		f = open(prefix + str(i+1),'r')
		data = f.read()
		output = StringIO.StringIO()
		output.write(data)
#		print output.getvalue().encode('hex')
		inputs.append(output)


	for i in xrange(k):
		inputs[i].seek(0)

	output = StringIO.StringIO()
	decode(inputs,output)

	#if(sharedsecret == output.getvalue()):
	print output.getvalue()
	print 'Recovered key is in file ./RecoveredKey'
	f=open('RecoveredKey','w')
	f.write(output.getvalue())


