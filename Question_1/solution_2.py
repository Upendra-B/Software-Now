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
    encrypted_chars = []  # stores encrypted characters
    rules = []            # stores transformation rules

    for c in text:
        # Case 1: lowercase letters
        if 'a' <= c <= 'z':
            if c <= 'm':  # first half of alphabet
                encrypted_chars.append(shift_char(c, shift1 * shift2))
                rules.append("L1")
            else:  # second half
                encrypted_chars.append(shift_char(c, -(shift1 + shift2)))
                rules.append("L2")

        # Case 2: uppercase letters
        elif 'A' <= c <= 'Z':
            if c <= 'M':
                encrypted_chars.append(shift_char(c, -shift1))
                rules.append("U1")
            else:
                encrypted_chars.append(shift_char(c, shift2 ** 2))
                rules.append("U2")

        # Case 3: non-alphabetic
        else:
            encrypted_chars.append(c)
            rules.append("O")

    return ''.join(encrypted_chars), rules


# Decryption using rule array
def decrypt_text(ciphertext: str, shift1: int, shift2: int, rules: list[str]) -> str:
    decrypted_chars = []
    for c, rule in zip(ciphertext, rules):
        if rule == "L1":
            decrypted_chars.append(shift_char(c, -(shift1 * shift2)))
        elif rule == "L2":
            decrypted_chars.append(shift_char(c, (shift1 + shift2)))
        elif rule == "U1":
            decrypted_chars.append(shift_char(c, shift1))
        elif rule == "U2":
            decrypted_chars.append(shift_char(c, -(shift2 ** 2)))
        elif rule == "O":
            decrypted_chars.append(c)
    return ''.join(decrypted_chars)


# File handling
def encrypt_file(base_dir: Path, shift1: int, shift2: int) -> tuple[Path, list[str]]:
    raw_path = base_dir / "raw_text.txt"
    enc_path = base_dir / "encrypted_text.txt"

    text = raw_path.read_text(encoding="utf-8")
    encrypted, rules = encrypt_text(text, shift1, shift2)
    enc_path.write_text(encrypted, encoding="utf-8")
    return enc_path, rules


def decrypt_file(base_dir: Path, shift1: int, shift2: int, rules: list[str]) -> Path:
    enc_path = base_dir / "encrypted_text.txt"
    dec_path = base_dir / "decrypted_text.txt"

    ciphertext = enc_path.read_text(encoding="utf-8")
    plaintext = decrypt_text(ciphertext, shift1, shift2, rules)
    dec_path.write_text(plaintext, encoding="utf-8")
    return dec_path


def verify(base_dir: Path) -> bool:
    raw_path = base_dir / "raw_text.txt"
    dec_path = base_dir / "decrypted_text.txt"
    return raw_path.read_text(encoding="utf-8") == dec_path.read_text(encoding="utf-8")


# Quick test function
def test_encrypt_decrypt():
    sample = "Hello World!"
    enc, rules = encrypt_text(sample, 2, 3)
    dec = decrypt_text(enc, 2, 3, rules)
    assert dec == sample, f"Test failed! Expected {sample}, got {dec}"
    print("🧪 Test passed: Encryption and decryption work correctly.")


# Main program
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    raw_path = base_dir / "raw_text.txt"

    if not raw_path.exists():
        print(f"❌ Error: {raw_path.name} does not exist in {base_dir}")
        raise SystemExit(1)

    # Input with validation
    while True:
        try:
            shift1 = int(input("Enter shift1 (integer): "))
            shift2 = int(input("Enter shift2 (integer): "))
            break
        except ValueError:
            print("❌ Invalid input! Please enter numbers only.")

    # Run test first
    test_encrypt_decrypt()

    # Perform encryption/decryption
    enc_path, rules = encrypt_file(base_dir, shift1, shift2)
    decrypt_file(base_dir, shift1, shift2, rules)

    if verify(base_dir):
        print("✅ Decryption successful! raw_text.txt and decrypted_text.txt match.")
    else:
        print("❌ Decryption failed! Files do not match.")

    print("\n📂 Files written:")
    print(f" - {enc_path}")
    print(f" - {base_dir / 'decrypted_text.txt'}")
