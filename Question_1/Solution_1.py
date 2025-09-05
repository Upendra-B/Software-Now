# solution1.py — improved version (edited by Sangam Dhungana)
from pathlib import Path
from typing import Callable

# Constant for alphabet size
ALPHA = 26


def _norm(n: int) -> int:
    # Keep any number inside 0–25 range
    return n % ALPHA


def _shift_lower(ch: str, n: int) -> str:
    # Shift a lowercase letter by n steps (wraps around)
    return chr((ord(ch) - ord('a') + n) % ALPHA + ord('a'))


def _shift_upper(ch: str, n: int) -> str:
    # Shift an uppercase letter by n steps (wraps around)
    return chr((ord(ch) - ord('A') + n) % ALPHA + ord('A'))


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Apply encryption rules based on character type:
      - a..m → forward by shift1 * shift2
      - n..z → backward by shift1 + shift2
      - A..M → backward by shift1
      - N..Z → forward by shift2 squared
      - anything else → no change
    """
    if 'a' <= ch <= 'z':
        if ch <= 'm':
            return _shift_lower(ch, _norm(shift1 * shift2))
        else:
            return _shift_lower(ch, -_norm(shift1 + shift2))
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':
            return _shift_upper(ch, -_norm(shift1))
        else:
            return _shift_upper(ch, _norm(shift2 ** 2))
    return ch


def decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    # Reverse of encrypt_char – brings characters back to original
    if 'a' <= ch <= 'z':
        if ch <= 'm':
            return _shift_lower(ch, -_norm(shift1 * shift2))
        else:
            return _shift_lower(ch, _norm(shift1 + shift2))
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':
            return _shift_upper(ch, _norm(shift1))
        else:
            return _shift_upper(ch, -_norm(shift2 ** 2))
    return ch


def _transform_file(src: Path, dst: Path,
                    func: Callable[[str, int, int], str],
                    s1: int, s2: int) -> None:
    # Read a file, transform each character, and write to a new file
    text = src.read_text(encoding="utf-8")
    out = "".join(func(ch, s1, s2) for ch in text)
    dst.write_text(out, encoding="utf-8")


def verify_files(file1: Path, file2: Path) -> bool:
    # Compare two files and return True only if their contents match
    return file1.read_text(encoding="utf-8") == file2.read_text(encoding="utf-8")


def _read_int(prompt: str) -> int:
    # Ask user for integer input until they type a valid number
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number (e.g., 3, 10, -4).")


def main() -> None:
    # Setup file paths
    base = Path(__file__).resolve().parent
    raw = base / "raw_text.txt"
    enc = base / "encrypted_text.txt"
    dec = base / "decrypted_text.txt"

    # Check if raw file exists
    if not raw.exists():
        print(f"❌ '{raw.name}' not found in {base}")
        print("   Put raw_text.txt next to solution1.py and run again.")
        return

    # Ask for shift values
    s1 = _read_int("Enter shift1 (int): ")
    s2 = _read_int("Enter shift2 (int): ")

    # Encrypt → Decrypt → Verify
    _transform_file(raw, enc, encrypt_char, s1, s2)
    print(f"🔒 Encryption complete → {enc.name}")

    _transform_file(enc, dec, decrypt_char, s1, s2)
    print(f"🔓 Decryption complete → {dec.name}")

    print("✅ Decryption verified successfully!"
          if verify_files(raw, dec) else
          "❌ Verification failed.")


if __name__ == "__main__":
    main()
