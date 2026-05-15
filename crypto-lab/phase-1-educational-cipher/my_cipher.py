message = "HELLO"
secret = 3

scrambled = ""
for letter in message:
    number = ord(letter)
    new_number = number + secret
    scrambled = scrambled + chr(new_number)

print("Original :", message)
print("Scrambled:", scrambled)

unscrambled = ""
for letter in scrambled:
    number = ord(letter)
    new_number = number - secret
    unscrambled = unscrambled + chr(new_number)

print("Unscrambled:", unscrambled)
print()
print("--- An attacker tries to crack KHOOR without knowing the key ---")

wrong_guess = 5
attacker_result = ""
for letter in scrambled:
    number = ord(letter)
    new_number = number - wrong_guess
    attacker_result = attacker_result + chr(new_number)

print("Attacker guessed", wrong_guess, "and got:", attacker_result)
print()
print("--- Attacker brute-forces ALL possible keys ---")

for guess in range(1, 26):
    cracked = ""
    for letter in scrambled:
        cracked = cracked + chr(ord(letter) - guess)
    print("Key", guess, "->", cracked)
