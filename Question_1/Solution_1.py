# solution1.py — hardened version (edited by Sangam Dhungana)
from pathlib import Path
from typing import Callable

ALPHA = 26


def _norm(n: int) -> int:
    """Normalize any integer shift to the 0..25 range."""
    return n % ALPHA


def _shift_lower(ch: str, n: int) -> str:
    """Shift a lowercase letter by n positions (wrap within a..z)."""
    return chr((ord(ch) - ord('a') + n) % ALPHA + ord('a'))


def _shift_upper(ch: str, n: int) -> str:
    """Shift an uppercase letter by n positions (wrap within A..Z)."""
    return chr((ord(ch) - ord('A') + n) % ALPHA + ord('A'))


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Encryption rules:
      - a..m  → forward by shift1 * shift2
      - n..z  → backward by shift1 + shift2
      - A..M  → backward by shift1
      - N..Z  → forward by (shift2 ** 2)
      - others unchanged
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
    """Exact inverse of encrypt_char."""
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
    """Read src, transform char-by-char with func, write dst."""
    text = src.read_text(encoding="utf-8")
    out = "".join(func(ch, s1, s2) for ch in text)
    dst.write_text(out, encoding="utf-8")


def verify_files(file1: Path, file2: Path) -> bool:
    """Return True iff file1 and file2 have identical text (UTF-8)."""
    return file1.read_text(encoding="utf-8") == file2.read_text(encoding="utf-8")


def _read_int(prompt: str) -> int:
    """Prompt until the user enters a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number (e.g., 3, 10, -4).")


def main() -> None:
    base = Path(__file__).resolve().parent
    raw = base / "raw_text.txt"
    enc = base / "encrypted_text.txt"
    dec = base / "decrypted_text.txt"

    if not raw.exists():
        print(f"❌ '{raw.name}' not found in {base}")
        print("   Put raw_text.txt next to solution1.py and run again.")
        return

    s1 = _read_int("Enter shift1 (int): ")
    s2 = _read_int("Enter shift2 (int): ")

    _transform_file(raw, enc, encrypt_char, s1, s2)
    print(f"🔒 Encryption complete → {enc.name}")

    _transform_file(enc, dec, decrypt_char, s1, s2)
    print(f"🔓 Decryption complete → {dec.name}")

    print("✅ Decryption verified successfully!"
          if verify_files(raw, dec) else
          "❌ Verification failed.")


if __name__ == "__main__":
    main()
