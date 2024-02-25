def encrypt(text):
    return ''.join(hex(ord(char))[2:] for char in text)

def decrypt(hex):
    return bytes.fromhex(hex).decode('utf-8')