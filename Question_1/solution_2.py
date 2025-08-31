from pathlib import Path

# -------------------------------------------------
# Helper function: shift a single letter with wrap
# -------------------------------------------------
def shift_char(c: str, shift: int) -> str:
    if 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:
        return c


# -------------------------------------------------
# Encryption with MASK
# -------------------------------------------------
def encrypt_text(text: str, shift1: int, shift2: int) -> tuple[str, str]:
    encrypted_chars = []
    mask_chars = []

    for c in text:
        if 'a' <= c <= 'z':
            if c <= 'm':  # lowercase first half
                encrypted_chars.append(shift_char(c, shift1 * shift2))
                mask_chars.append("a")
            else:         # lowercase second half
                encrypted_chars.append(shift_char(c, -(shift1 + shift2)))
                mask_chars.append("b")
        elif 'A' <= c <= 'Z':
            if c <= 'M':  # uppercase first half
                encrypted_chars.append(shift_char(c, -shift1))
                mask_chars.append("A")
            else:         # uppercase second half
                encrypted_chars.append(shift_char(c, shift2 ** 2))
                mask_chars.append("B")
        else:             # non-letter
            encrypted_chars.append(c)
            mask_chars.append("-")

    return ''.join(encrypted_chars), ''.join(mask_chars)


# -------------------------------------------------
# Decryption with MASK
# -------------------------------------------------
def decrypt_text(ciphertext: str, mask: str, shift1: int, shift2: int) -> str:
    decrypted_chars = []

    for c, tag in zip(ciphertext, mask):
        if tag == "a":  # lowercase first half
            decrypted_chars.append(shift_char(c, -(shift1 * shift2)))
        elif tag == "b":  # lowercase second half
            decrypted_chars.append(shift_char(c, (shift1 + shift2)))
        elif tag == "A":  # uppercase first half
            decrypted_chars.append(shift_char(c, shift1))
        elif tag == "B":  # uppercase second half
            decrypted_chars.append(shift_char(c, -(shift2 ** 2)))
        else:  # non-letter
            decrypted_chars.append(c)

    return ''.join(decrypted_chars)


# -------------------------------------------------
# File Operations
# -------------------------------------------------
def encrypt_file(base_dir: Path, shift1: int, shift2: int):
    raw_path = base_dir / "raw_text.txt"
    enc_path = base_dir / "encrypted_text.txt"
    mask_path = base_dir / "mask.txt"

    text = raw_path.read_text(encoding="utf-8")
    encrypted, mask = encrypt_text(text, shift1, shift2)

    enc_path.write_text(encrypted, encoding="utf-8")
    mask_path.write_text(mask, encoding="utf-8")

    return enc_path, mask_path


def decrypt_file(base_dir: Path, shift1: int, shift2: int):
    enc_path = base_dir / "encrypted_text.txt"
    mask_path = base_dir / "mask.txt"
    dec_path = base_dir / "decrypted_text.txt"

    ciphertext = enc_path.read_text(encoding="utf-8")
    mask = mask_path.read_text(encoding="utf-8")

    plaintext = decrypt_text(ciphertext, mask, shift1, shift2)
    dec_path.write_text(plaintext, encoding="utf-8")

    return dec_path


def verify(base_dir: Path) -> bool:
    raw_path = base_dir / "raw_text.txt"
    dec_path = base_dir / "decrypted_text.txt"

    return raw_path.read_text(encoding="utf-8") == dec_path.read_text(encoding="utf-8")


# -------------------------------------------------
# Main program
# -------------------------------------------------
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent

    # Create a sample raw_text.txt if missing
    raw_path = base_dir / "raw_text.txt"
    if not raw_path.exists():
        raw_path.write_text("Hello World!\nThis is a default test message.\nABC xyz", encoding="utf-8")
        print(f"Created sample file: {raw_path}")

    # Ask for user inputs
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    # Encrypt -> Decrypt -> Verify
    encrypt_file(base_dir, shift1, shift2)
    decrypt_file(base_dir, shift1, shift2)

    if verify(base_dir):
        print("✅ Decryption successful! The files match.")
    else:
        print("❌ Decryption failed! The files do not match.")

    print("\nFiles written in folder:")
    print(f" - raw_text.txt")
    print(f" - encrypted_text.txt")
    print(f" - mask.txt")
    print(f" - decrypted_text.txt")
