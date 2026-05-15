from cryptography.fernet import Fernet

# 1. Generate a key (this is the Encryption Key from your diagram)
key = Fernet.generate_key()
print("Key       :", key)

# 2. Create a Fernet "lockbox" using that key
lockbox = Fernet(key)

# 3. Encrypt a message
message = b"My SOC analyst notes - top secret"
ciphertext = lockbox.encrypt(message)
print("Ciphertext:", ciphertext)

# 4. Decrypt it back
plaintext = lockbox.decrypt(ciphertext)
print("Plaintext :", plaintext)
from cryptography.fernet import InvalidToken

# What if an attacker tampers with the ciphertext?
print()
print("--- Attacker tampers with the ciphertext ---")
tampered = ciphertext[:-4] + b"AAAA"  # change the last 4 bytes
try:
    lockbox.decrypt(tampered)
    print("Decryption succeeded - that should NOT happen!")
except InvalidToken:
    print("Tamper detected - decryption refused")

# What if an attacker has the ciphertext but the wrong key?
print()
print("--- Attacker tries with the wrong key ---")
wrong_key = Fernet.generate_key()
wrong_lockbox = Fernet(wrong_key)
try:
    wrong_lockbox.decrypt(ciphertext)
    print("Decryption succeeded - that should NOT happen!")
except InvalidToken:
    print("Wrong key - decryption refused")

