import hashlib
import os

filename = "secret_note.txt"
baseline_file = "baseline.txt"

# Step 1: hash the file as it exists right now
with open(filename, "rb") as f:
    current_fingerprint = hashlib.sha256(f.read()).hexdigest()

# Step 2: do we already have a baseline saved?
if not os.path.exists(baseline_file):
    # First run - save this fingerprint as the trusted baseline
    with open(baseline_file, "w") as f:
        f.write(current_fingerprint)
    print("Baseline created for:", filename)
    print("Fingerprint saved   :", current_fingerprint)
else:
    # Baseline exists - compare current to saved
    with open(baseline_file, "r") as f:
        saved_fingerprint = f.read()

    print("File        :", filename)
    print("Saved hash  :", saved_fingerprint)
    print("Current hash:", current_fingerprint)
    print()

    if saved_fingerprint == current_fingerprint:
        print("STATUS: OK - file unchanged")
    else:
        print("STATUS: ALERT - FILE HAS BEEN MODIFIED!")
