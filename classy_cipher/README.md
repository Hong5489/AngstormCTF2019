# Classy Cipher
Description:

Every CTF starts off with a Caesar cipher, but we're more [classy](classy_cipher.c).

Author: defund

Open the source code:
```python
from secret import flag, shift

def encrypt(d, s):
	e = ''
	for c in d:
		e += chr((ord(c)+s) % 0xff)
	return e

assert encrypt(flag, shift) == ':<M?TLH8<A:KFBG@V'
```

Calculate the distance between `:` and `a` because the flag starts with `a`
```python
>>> ord(':') - ord('a')
-39
```
Using the same function to get the flag:
```python
print encrypt(':<M?TLH8<A:KFBG@V',39)
```
[Full script](solve.py)

## Flag
> actf{so_charming}