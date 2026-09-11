import re
#hexaPattern = re.compile(r'\s([0-9a-fA-F]+))?\s')
hexaPattern = re.compile(r'([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s([0-9a-fA-F][0-9a-fA-F])\s')

# Create an array of bytes you want in your ROM
# Example: 16 Kilobytes filled with 0xFF (often used as padding)
rom_size = 2 * 1024
data = bytearray([0xFF] * rom_size)

# Read the ROM text file
count = 0
# https://stackoverflow.com/questions/9282967/how-to-open-a-file-using-the-open-with-statement
with open("rom.txt", "rt") as infile:
    #f.read(line)
    for line in infile:
        # https://stackoverflow.com/questions/10270407/regular-expression-for-hexadecimal-string-in-python-not-working
        m = re.search(hexaPattern, line)
        if m:
           print("found a match:", m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), m.group(8))
           shortline = m.group(1)+ m.group(2)+ m.group(3)+ m.group(4)+ m.group(5)+ m.group(6)+ m.group(7)+ m.group(8)
           print("shortline:", shortline)

     
        # from https://stackoverflow.com/questions/5649407/how-to-convert-hexadecimal-string-to-bytes-in-python
        bytes = bytearray.fromhex(shortline)  # remove the address from the start of the line first?
        data[count] = bytes[0]
        data[count+1] = bytes[1]
        data[count+2] = bytes[2]
        data[count+3] = bytes[3]
        data[count+4] = bytes[4]
        data[count+5] = bytes[5]
        data[count+6] = bytes[6]
        data[count+7] = bytes[7]
        count = count + 8

# Insert your custom data or machine instructions at specific offsets
#data[0] = 0x41  # 'A'
#data[1] = 0x42  # 'B' (An example custom header)

# Write the data to a .bin file
with open("my_custom_rom.bin", "wb") as f:
    f.write(data)

