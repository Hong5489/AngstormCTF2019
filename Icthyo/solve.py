from PIL import Image

image = Image.open('out.png')
rgb = image.convert('RGB')

imageArray = []

for i in range(image.width):
	for j in range(image.height):
		imageArray.append(rgb.getpixel((j,i)))
flag = ''
for rowValue in range(0x100):
	bits = ''
	for counter in range(8):
		index = (rowValue*256) + (counter*32)
		r,g,b = imageArray[index]
		bits = str(((g^r) & 1) ^ (b & 1)) + bits
	flag += chr(int(bits,2))
print flag