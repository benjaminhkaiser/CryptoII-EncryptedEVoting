#!/usr/bin/python
from charm.toolbox import secretshare
from charm.toolbox.pairinggroup import PairingGroup,ZR,order
k=3
n=4
group = PairingGroup('SS512')

s=secretshare.SecretShare(group,False)
sec=group.random(ZR)
sec=5
shares = s.genShares(sec,k,n)

orig=shares[0]
print("original:%s" % orig)

