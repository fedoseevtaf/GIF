from lzw import *


# Byte code of the file
bc = bytearray()

# Signature
bc.extend(b'GIF87a')

# Screen size definition (2 x 2)
bc.extend(reversed((2   ).to_bytes(2, 'big')))
bc.extend(reversed((2   ).to_bytes(2, 'big')))

bc.append(0b11110001)
bc.extend(b'\x01\x00')

# Color map
bc.extend(b'\x00\x00\x00')
bc.extend(b'\x00\xff\xff')
bc.extend(b'\xff\x00\xff')
bc.extend(b'\xff\xff\x00')

# First image:
# Image start character
bc.extend(b',')

# Position definition (0 x 0)
bc.extend(b'\x00\x00\x00\x00')
# Image size definition (2 x 2)
bc.extend(reversed((2   ).to_bytes(2, 'big')))
bc.extend(reversed((2   ).to_bytes(2, 'big')))
bc.append(0b00000000)

# Color index bit length in [2;8] ∩ N
bc.append(2)

data = 3, 2, 2, 1
data = lzw(data)
data = packlzw(data)
data = packbytes(data)
bc.extend(data)

bc.append(0)

# GIF terminator character
bc.extend(b';')

with open('first.gif', 'wb') as file:
    file.write(bc)


#














































