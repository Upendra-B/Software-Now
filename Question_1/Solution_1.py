import string
import os

# ---------- Encryption Function ----------
def encrypt(text, shift1, shift2):
    encrypted = ""
    for char in text:
        # Lowercase letters
        if char.islower():
            if char in string.ascii_lowercase[:13]:  # a-m
                shift = shift1 * shift2
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:  # n-z
                shift = shift1 + shift2
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            encrypted += new_char

        # Uppercase letters
        elif char.isupper():
            if char in string.ascii_uppercase[:13]:  # A-M
                shift = shift1
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:  # N-Z
                shift = shift2 ** 2
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            encrypted += new_char

        else:
            # Keep numbers, spaces, symbols unchanged
            encrypted += char

    return encrypted


# ---------- Decryption Function ----------
def decrypt(text, shift1, shift2):
    decrypted = ""
    for char in text:
        # Lowercase letters
        if char.islower():
            if char in string.ascii_lowercase[:13]:  # a-m
                shift = shift1 * shift2
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:  # n-z
                shift = shift1 + shift2
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            decrypted += new_char

        # Uppercase letters
        elif char.isupper():
            if char in string.ascii_uppercase[:13]:  # A-M
                shift = shift1
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:  # N-Z
                shift = shift2 ** 2
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            decrypted += new_char

        else:
            decrypted += char

    return decrypted


# ---------- Verification Function ----------
def verify(original_file, decrypted_file):
    with open(original_file, "r") as f1, open(decrypted_file, "r") as f2:
        if f1.read() == f2.read():
            print("✅ Decryption successful! Files match.")
        else:
            print("❌ Decryption failed! Files do not match.")


# ---------- Main Program ----------
def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Auto-create raw_text.txt if it doesn't exist
    if not os.path.exists("raw_text.txt"):
        with open("raw_text.txt", "w") as f:
            f.write("Hello World!\nThis is a test message 123.")
        print("⚠️ raw_text.txt not found. A sample file has been created.")

    # Read raw text
    with open("raw_text.txt", "r") as f:
        raw_text = f.read()

    # Encrypt and write to file
    encrypted_text = encrypt(raw_text, shift1, shift2)
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted_text)
    print("🔒 Encrypted text saved to encrypted_text.txt")

    # Decrypt and write to file
    decrypted_text = decrypt(encrypted_text, shift1, shift2)
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted_text)
    print("🔓 Decrypted text saved to decrypted_text.txt")

    # Verify result
    verify("raw_text.txt", "decrypted_text.txt")


# Run the program
if __name__ == "__main__":
    main()
