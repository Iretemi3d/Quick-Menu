input = "inw|}ba)kF( F(w"

output = ""

for i in range(len(input)):
    print(chr(0x19^ord(input[i])), end="")