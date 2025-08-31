import os

# Helper: shift a character by n places with wraparound
def shift_char(c, shift):
    if c.islower():
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif c.isupper():
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c

# Encryption function
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as infile:
        text = infile.read()

    encrypted_text = ""
    for c in text:
        if c.islower():
            if c <= 'm':
                encrypted_text += shift_char(c, shift1 * shift2)
            else:
                encrypted_text += shift_char(c, -(shift1 + shift2))
        elif c.isupper():
            if c <= 'M':
                encrypted_text += shift_char(c, -shift1)
            else:
                encrypted_text += shift_char(c, shift2 ** 2)
        else:
            encrypted_text += c

    with open("encrypted_text.txt", "w", encoding="utf-8") as outfile:
        outfile.write(encrypted_text)
'''
# Decryption function
def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as infile:
        text = infile.read()

    decrypted_text = ""
    for c in text:
        if c.islower():
            if c <= 'm':
                decrypted_text += shift_char(c, -(shift1 * shift2))
            else:
                decrypted_text += shift_char(c, shift1 + shift2)
        elif c.isupper():
            if c <= 'M':
                decrypted_text += shift_char(c, shift1)
            else:
                decrypted_text += shift_char(c, -(shift2 ** 2))
        else:
            decrypted_text += c

    with open("decrypted_text.txt", "w", encoding="utf-8") as outfile:
        outfile.write(decrypted_text)
'''
if __name__ == "__main__":
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    # decrypt_file(shift1, shift2)
