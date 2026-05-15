"""
Crypto Lab - Encrypt / Decrypt
Maps directly to the ISC2 CC Domain 5 diagram (Hashing & Encryption).

Diagram box            ->  Code below
---------------------      ----------------------------------
Plaintext              ->  the message string you pass in
Encryption Key         ->  derived from your password (derive_key)
Cryptovariables        ->  salt + nonce (random values, not secret)
Key Management         ->  derive_key(): turns a password into a key
Encryption Algorithm   ->  encrypt(): keystream XOR + HMAC tag
Ciphertext             ->  the scrambled bytes (token) you get back
Decryption Key         ->  SAME key, re-derived from the same password
Decryption Algorithm   ->  decrypt(): re-creates keystream, reverses XOR

This is an EDUCATIONAL stream cipher built only from Python's standard
library so it runs with zero installs. It is NOT production crypto.
For real work, use the `cryptography` library (see notes at the bottom).
"""

import hashlib
import hmac
import secrets
import base64


# --- KEY MANAGEMENT ---------------------------------------------------
# A password is something a human remembers. A key is what the algorithm
# needs. Key management is the bridge: stretch the password into a key.
# PBKDF2 runs the hash 200,000 times so guessing passwords is slow.
def derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)


# --- ENCRYPTION ALGORITHM ---------------------------------------------
# Build a keystream (pseudo-random bytes) from the key + nonce, then XOR
# it against the plaintext. XOR is reversible: doing it twice with the
# same keystream gets you back the original.
def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    out = b""
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest()
        out += block
        counter += 1
    return out[:length]


def encrypt(plaintext: str, password: str) -> str:
    # Cryptovariables: random, fresh every time, NOT secret. They make
    # sure encrypting the same message twice gives different ciphertext.
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(16)

    key = derive_key(password, salt)                       # Encryption Key
    data = plaintext.encode()
    keystream = _keystream(key, nonce, len(data))
    ciphertext = bytes(a ^ b for a, b in zip(data, keystream))

    # INTEGRITY (right-hand box in your screenshot): an HMAC tag. If even
    # one byte of the ciphertext is changed, this check fails on decrypt.
    tag = hmac.new(key, salt + nonce + ciphertext, hashlib.sha256).digest()

    # Ciphertext token = everything the receiver needs, base64-encoded.
    token = base64.b64encode(salt + nonce + tag + ciphertext)
    return token.decode()


# --- DECRYPTION ALGORITHM ---------------------------------------------
def decrypt(token: str, password: str) -> str:
    raw = base64.b64decode(token)
    salt, nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:64], raw[64:]

    key = derive_key(password, salt)                       # Decryption Key

    # Verify integrity BEFORE decrypting. Wrong password or tampered data
    # both fail here.
    expected = hmac.new(key, salt + nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("Integrity check failed: wrong password or tampered data")

    keystream = _keystream(key, nonce, len(ciphertext))
    plaintext = bytes(a ^ b for a, b in zip(ciphertext, keystream))
    return plaintext.decode()


# --- TRY IT -----------------------------------------------------------
if __name__ == "__main__":
    message = "Olayinka - SOC analyst in training"
    password = "correct horse battery staple"

    print("Plaintext :", message)

    token = encrypt(message, password)
    print("Ciphertext:", token)

    recovered = decrypt(token, password)
    print("Decrypted :", recovered)

    # Prove the integrity check works: flip one character of the token.
    tampered = token[:-2] + ("AA" if token[-2:] != "AA" else "BB")
    try:
        decrypt(tampered, password)
    except ValueError as e:
        print("Tamper test:", e)

# --- DOING THIS FOR REAL ----------------------------------------------
# pip install cryptography
#
#   from cryptography.fernet import Fernet
#   key = Fernet.generate_key()      # Encryption Key + Key Management
#   f = Fernet(key)
#   token = f.encrypt(b"secret")     # Encryption Algorithm -> Ciphertext
#   f.decrypt(token)                 # Decryption Algorithm -> Plaintext
#
# Fernet uses AES (a vetted algorithm) and handles cryptovariables and
# the integrity tag for you. Always prefer vetted libraries over
# hand-rolled crypto in real systems.
