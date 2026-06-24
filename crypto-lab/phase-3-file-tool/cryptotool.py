import argparse

# Set up the command-line interface
parser = argparse.ArgumentParser(description="Encrypt or decrypt a file with a password")
parser.add_argument("action", choices=["encrypt", "decrypt"], help="What to do")
parser.add_argument("filename", help="The file to encrypt or decrypt")

# Read what the user typed
args = parser.parse_args()

# For now, just print what we got
print("Action  :", args.action)
print("Filename:", args.filename)
