# Icthyo
Description:

Long before stegosaurus roamed the earth, another [species](icthyo) prowled the sea; here is an artist's [rendition](out.png).

Type `strings icthyo` we saw some interesting things
```
...
%s must be 256 x 256
%s must be 8 bit depth
%s must be RGB
message (less than 256 bytes): 
USAGE: %s in.png out.png
...
```
We guess it will hide some message in the `out.png` using `in.png`

We created a `white.png` with size of 256 x 256 to test the function
```bash
./icthyo white.png sample.png
message (less than 256 bytes): hello
```
It just prompt for the message to hide and exit

We open this in Ghidra and decompile it, the main function:
```c
int main(int iParm1,undefined8 *puParm2)

{
  time_t tVar1;
  
  if (iParm1 != 3) {
    printf("USAGE: %s in.png out.png\n",*puParm2);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  read_file(puParm2[1]);
  encode();
  write_file(puParm2[2]);
  return 0;
}
```
Look at the encode function looks complicated:
```c
void encode(void)

{
  char cVar1;
  int iVar2;
  byte *pbVar3;
  long lVar4;
  undefined8 *puVar5;
  long in_FS_OFFSET;
  int rowValue;
  int colValue;
  int counter;
  undefined8 local_118 [33];
  long local_10;
  long currentRow;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  lVar4 = 0x20;
  puVar5 = local_118;
  while (lVar4 != 0) {
    lVar4 = lVar4 + -1;
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  printf("message (less than 256 bytes): ");
  fgets((char *)local_118,0x100,stdin);
  rowValue = 0;
  while (rowValue < 0x100) {
    currentRow = *(long *)(rows + (long)rowValue * 8);
    colValue = 0;
    while (colValue < 0x100) {
      pbVar3 = (byte *)(currentRow + (long)(colValue * 3));
      iVar2 = rand();
      *pbVar3 = (byte)iVar2 & 1 ^ *pbVar3;
      iVar2 = rand();
      pbVar3[1] = pbVar3[1] ^ (byte)iVar2 & 1;
      iVar2 = rand();
      pbVar3[2] = pbVar3[2] ^ (byte)iVar2 & 1;
      colValue = colValue + 1;
    }
    counter = 0;
    while (counter < 8) {
      pbVar3 = (byte *)(currentRow + (long)(counter * 0x60));
      cVar1 = *(char *)((long)local_118 + (long)rowValue);
      if ((pbVar3[2] & 1) != 0) {
        pbVar3[2] = pbVar3[2] ^ 1;
      }
      pbVar3[2] = pbVar3[2] |
                  (byte)((int)cVar1 >> ((byte)counter & 0x1f)) & 1 ^ (pbVar3[1] ^ *pbVar3) & 1;
      counter = counter + 1;
    }
    rowValue = rowValue + 1;
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
Basically it prompt the message to hide:
```c
printf("message (less than 256 bytes): ");
fgets((char *)local_118,0x100,stdin);
```
And add 1 or minus 1 to every column in every row:
```c
while (colValue < 0x100) {
      pbVar3 = (byte *)(currentRow + (long)(colValue * 3));
      iVar2 = rand();
      *pbVar3 = (byte)iVar2 & 1 ^ *pbVar3;
      iVar2 = rand();
      pbVar3[1] = pbVar3[1] ^ (byte)iVar2 & 1;
      iVar2 = rand();
      pbVar3[2] = pbVar3[2] ^ (byte)iVar2 & 1;
      colValue = colValue + 1;
}
```
And hide the message in specific coordinates in the output image:
```c
counter = 0;
while (counter < 8) {
  pbVar3 = (byte *)(currentRow + (long)(counter * 0x60));
  cVar1 = *(char *)((long)local_118 + (long)rowValue);
  if ((pbVar3[2] & 1) != 0) {
    pbVar3[2] = pbVar3[2] ^ 1;
  }
  pbVar3[2] = pbVar3[2] |
              (byte)((int)cVar1 >> ((byte)counter & 0x1f)) & 1 ^ (pbVar3[1] ^ *pbVar3) & 1;
  counter = counter + 1;
}
```
After we do some research for how C reads the image,
## Reference
[A simple libpng example program](http://zarb.org/~gc/html/libpng.html)

We realize `pbVar3` is the RGB value in the pixel which means:
```c
pbVar3[0] //is R
pbVar3[1] //is G
pbVar3[2] //is B
```
According to the code:
```c
if ((pbVar3[2] & 1) != 0) {		//if B is not even 
    pbVar3[2] = pbVar3[2] ^ 1;	//make it even
}
```
And the most complicated line here:
```c
pbVar3[2] = pbVar3[2] | (cVar1 >> (counter & 0x1f)) & 1 ^ (pbVar3[1] ^ pbVar3) & 1;
```
`cVar1` is the message char follow the current `rowValue`
```c
cVar1 = *(char *)((long)local_118 + (long)rowValue);
```
And the `cVar1` shift right number of `counter`:
```c
// If cVar1 is 'h'
// h in binary is 01101000
// shift right 1
01101000 -> 00110100
// shift right 2
01101000 -> 00011010
```
The `counter` start with `0` and loop until `7`

That means the `(cVar1 >> (counter & 0x1f))` is equal to `cVar1 >> counter`

Because `counter` doing bitwise to 0x1f has no effect if the value is 0 to 7

So the process looks like this:
```c
// If cVar1 is 'h'
// h in binary is 01101000
cVar1 >> 0	-> 01101000
cVar1 >> 1	->  0110100
cVar1 >> 2	->   011010
cVar1 >> 3	->    01101
cVar1 >> 4	->     0110
cVar1 >> 5	->      011
cVar1 >> 6	->       01
cVar1 >> 7	->        0
```
After that it perform bitwise AND for 1

Means if the last bit is `1` the result is `1`, if `0` the result is `0`
```c
cVar1 >> 0	-> 01101000 & 1 = 0
cVar1 >> 1	->  0110100 & 1 = 0
cVar1 >> 2	->   011010 & 1 = 0
cVar1 >> 3	->    01101 & 1 = 1
cVar1 >> 4	->     0110 & 1 = 0
cVar1 >> 5	->      011 & 1 = 1
cVar1 >> 6	->       01 & 1 = 1
cVar1 >> 7	->        0 & 1 = 0
```
If you arrange the result, you will see is exactly the same as the binary:
```
	       0
	      0
	     0
	    1
	   0
	  1
	 1
+	0
------------
	01101000
------------
```
But after that, the result will XOR with `(pbVar3[1] ^ pbVar3) & 1`

Which means if `(pbVar3[1] ^ pbVar3)` last bit is `1` and result is `1` then `1 XOR 1 = 0`
```c
1 ^ 1 = 0	//if cVar1 >> counter = 1 and (pbVar3[1] ^ pbVar3) = 1
1 ^ 0 = 1	//if cVar1 >> counter = 1 and (pbVar3[1] ^ pbVar3) = 0
0 ^ 1 = 1	//if cVar1 >> counter = 0 and (pbVar3[1] ^ pbVar3) = 1
0 ^ 0 = 0	//if cVar1 >> counter = 0 and (pbVar3[1] ^ pbVar3) = 0
```
Lastly it perform OR bitwise with the result:
```c
//if pbVar3[2] (B) is 255
if ((pbVar3[2] & 1) != 0) {		//if B last bit is 1
    pbVar3[2] = pbVar3[2] ^ 1;	//B last bit become 0, 255 - 1 = 254
}
pbVar3[2] = 254 | 0 = 254
pbVar3[2] = 254 | 1 = 255
```
Summarize the equation:
```c
B = B | message & 1 ^ (G ^ R) & 1
```
It got four possible:
```c
1 & 1 ^ 1 & 1 = B add 0 means B is even or last bit is 0
1 & 1 ^ 0 & 1 = B add 1 means B is odd or last bit is 1
0 & 1 ^ 1 & 1 = B add 1 means B is odd or last bit is 1
0 & 1 ^ 0 & 1 = B add 0 means B is even or last bit is 0
```
Our target is to find message

Simplify the equation:
```c
B = message ^ (G ^ R)
message = B ^ (G ^ R)
``` 
So if we know the RGB value, we can find the message!

I wrote a [python script](solve.py) that uses PIL to get all the pixel RGB value

And we get the flag!!!
```bash
python solve.py 
actf{lurking_in_the_depths_of_random_bits}
```

## Flag
> actf{lurking_in_the_depths_of_random_bits}