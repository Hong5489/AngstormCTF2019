def encrypt(d, s):
	e = ''
	for c in d:
		e += chr((ord(c)+s) % 0xff)
	return e

print encrypt(':<M?TLH8<A:KFBG@V',39)