import os

def encrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'z':
        if ch <= 'm':  # first half
            return chr((ord(ch) - ord('a') + (shift1 * shift2)) % 26 + ord('a'))
        else:  # second half
            return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':  # first half
            return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A'))
        else:  # second half
            return chr((ord(ch) - ord('A') + (shift2 ** 2)) % 26 + ord('A'))
    else:
        return ch

def decrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'z':
        if ch <= 'm':  # this was originally a–m → reverse + shift
            return chr((ord(ch) - ord('a') - (shift1 * shift2)) % 26 + ord('a'))
        else:  # this was originally n–z → reverse − shift
            return chr((ord(ch) - ord('a') + (shift1 + shift2)) % 26 + ord('a'))
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':  # originally A–M
            return chr((ord(ch) - ord('A') + shift1) % 26 + ord('A'))
        else:  # originally N–Z
            return chr((ord(ch) - ord('A') - (shift2 ** 2)) % 26 + ord('A'))
    else:
        return ch

def encrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encrypted)

def decrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decrypted)

def verify_files(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        return f1.read() == f2.read()

def main():
    base = os.path.dirname(__file__)
    raw = os.path.join(base, "raw_text.txt")
    enc = os.path.join(base, "encrypted_text.txt")
    dec = os.path.join(base, "decrypted_text.txt")

    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(raw, enc, shift1, shift2)
    print("Encryption complete.")

    decrypt_file(enc, dec, shift1, shift2)
    print("Decryption complete.")

    if verify_files(raw, dec):
        print("Decryption verified successfully!")
    else:
        print("Verification failed.")

if __name__ == "__main__":
    main()
