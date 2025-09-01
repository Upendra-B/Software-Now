from pathlib import Path   # For handling file paths

# Simple shift function
def shift_char(c: str, shift: int) -> str:
    """
    Shifts a single character (c) by shift positions
    Works separately for lowercase [a-z] and uppercase [A-Z]
    If the character is not a letter it is returned unchanged
    """
    if 'a' <= c <= 'z':  # lowercase
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':  # uppercase
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c  # non-alphabetic characters remain the same


# Encryption with array
def encrypt_text(text: str, shift1: int, shift2: int) -> tuple[str, list[str]]:
    """
    Encrypts a given text using two shifts (shift1, shift2).
    Different rules are applied depending on:
      - lowercase first half (a-m)
      - lowercase second half (n-z)
      - uppercase first half (A-M)
      - uppercase second half (N-Z)
      - other characters (unchanged)

    Also generates a rules list storing which rules applied for encrption
    so that decryption can later be reversed exactly.
    """
    encrypted_chars = []  # stores encrypted characters
    rules = []            # stores transformation rules

    for c in text:
        # Case 1: lowercase letters
        if 'a' <= c <= 'z':
            if c <= 'm':  # first half of alphabet
                encrypted_chars.append(shift_char(c, shift1 * shift2))
                rules.append("L1")   # mark rule as lowercase-first-half
            else:  # second half of alphabet
                encrypted_chars.append(shift_char(c, -(shift1 + shift2)))
                rules.append("L2")   # mark rule as lowercase-second-half

        # Case 2: uppercase letters
        elif 'A' <= c <= 'Z':
            if c <= 'M':  # first half of alphabet
                encrypted_chars.append(shift_char(c, -shift1))
                rules.append("U1")   # mark rule as uppercase-first-half
            else:  # second half of alphabet
                encrypted_chars.append(shift_char(c, shift2 ** 2))
                rules.append("U2")   # mark rule as uppercase-second-half

        # Case 3: non-alphabetic characters
        else:
            encrypted_chars.append(c)  # no change
            rules.append("O")          # mark as 'other'

    # Return encrypted string and its rules
    return ''.join(encrypted_chars), rules


# Decryption using rule array
def decrypt_text(ciphertext: str, shift1: int, shift2: int, rules: list[str]) -> str:
    """
    Decrypts the ciphertext using the same shifts and the stored rule array
    Each character is reversed according to the exact rule used in encryption
    """
    decrypted_chars = []  # stores decrypted characters

    for c, rule in zip(ciphertext, rules):  # process char and its encryption rule
        if rule == "L1":
            decrypted_chars.append(shift_char(c, -(shift1 * shift2)))
        elif rule == "L2":
            decrypted_chars.append(shift_char(c, (shift1 + shift2)))
        elif rule == "U1":
            decrypted_chars.append(shift_char(c, shift1))
        elif rule == "U2":
            decrypted_chars.append(shift_char(c, -(shift2 ** 2)))
        elif rule == "O":
            decrypted_chars.append(c)  # unchanged

    return ''.join(decrypted_chars)


# File handling for reading/writing
def encrypt_file(base_dir: Path, shift1: int, shift2: int) -> tuple[Path, list[str]]:
    """
    Reads raw_text.txt encrypts it and writes encrypted_text.txt
    Returns the path to encrypted file and the rule array
    """
    raw_path = base_dir / "raw_text.txt"
    enc_path = base_dir / "encrypted_text.txt"

    # Read input text
    text = raw_path.read_text(encoding="utf-8")

    # Encrypt text and get rules
    encrypted, rules = encrypt_text(text, shift1, shift2)

    # Save encrypted text
    enc_path.write_text(encrypted, encoding="utf-8")
    return enc_path, rules


def decrypt_file(base_dir: Path, shift1: int, shift2: int, rules: list[str]) -> Path:
    """
    Reads encrypted_text.txt decrypts it using stored rules and writes decrypted_text.txt
    """
    enc_path = base_dir / "encrypted_text.txt"
    dec_path = base_dir / "decrypted_text.txt"

    # Read ciphertext
    ciphertext = enc_path.read_text(encoding="utf-8")

    # Decrypt text
    plaintext = decrypt_text(ciphertext, shift1, shift2, rules)

    # Save decrypted text
    dec_path.write_text(plaintext, encoding="utf-8")
    return dec_path


def verify(base_dir: Path) -> bool:
    """
    Compares raw_text.txt and decrypted_text.txt
    Returns True if both match else False
    """
    raw_path = base_dir / "raw_text.txt"
    dec_path = base_dir / "decrypted_text.txt"
    return raw_path.read_text(encoding="utf-8") == dec_path.read_text(encoding="utf-8")


# Main program
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent  # base directory of the script

    # Path for raw_text.txt
    raw_path = base_dir / "raw_text.txt"

    # If raw_text.txt does not exist show error and exit
    if not raw_path.exists():
        print(f"❌ Error: {raw_path.name} does not exist in {base_dir}")
        raise SystemExit(1)  # stop program immediately

    # User input for shifts
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Perform encryption and decryption
    enc_path, rules = encrypt_file(base_dir, shift1, shift2)
    decrypt_file(base_dir, shift1, shift2, rules)

    # Verify correctness
    if verify(base_dir):
        print("✅ Decryption successful! Files match.")
    else:
        print("❌ Decryption failed!")

    # Show generated files
    print("\nFiles written:")
    print(" - encrypted_text.txt")
    print(" - decrypted_text.txt")
