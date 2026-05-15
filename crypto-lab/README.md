# Crypto Lab — Encryption, Integrity, and Detection from the Ground Up

**A hands-on homelab that builds, then breaks, then properly secures cryptographic systems — turning the ISC2 CC Domain 5 diagram into working code, then extending it into a real SOC detection tool.**

Built by Olayinka as a portfolio project for Junior SOC Analyst roles. The goal isn't "I called an encryption library." The goal is **"I understand what every box in the crypto pipeline does, why hand-rolled crypto fails, what a vetted library does for me, and how to build the kind of detection tool a SOC analyst uses every day."**

---

## Why This Lab Exists

Most entry-level candidates can recite "confidentiality, integrity, availability." Very few can explain the difference between a password and a key, why a nonce matters, how an integrity tag catches tampering, or how file integrity monitoring works.

This lab closes that gap by working through the full pipeline from the ISC2 CC course — and going beyond it into practical detection engineering:

```
                  ┌──────────────┐                    ┌──────────────┐
   Plaintext ───> │  Encryption  │ ──> Ciphertext ──> │  Decryption  │ ──> Plaintext
                  │  Algorithm   │                    │  Algorithm   │
                  └──────┬───────┘                    └──────┬───────┘
                         │                                   │
              Encryption Key + Cryptovariables     Decryption Key + Cryptovariables
                         │                                   │
                  ┌──────┴───────────────── Key Management ───┴──────┐
                  │   password ──PBKDF2──> key   |   key storage     │
                  └───────────────────────────────────────────────────┘
```

---

## Status

| # | Component | Status | Deliverable |
|---|-----------|--------|-------------|
| 1 | Educational Cipher (Caesar) | ✅ Done | Hand-built cipher proving every concept; brute-force attack proves why it's weak |
| 2 | Real Crypto (AES via Fernet) | ✅ Done | Production-grade encryption with automatic integrity protection |
| 3 | File Integrity Monitor v1 | ✅ Done | Working SOC-style tool that detects file tampering via SHA-256 hashing |
| 4 | File Integrity Monitor v2 | 🔄 Next | Extend FIM to scan whole folders — detects new, modified, AND deleted files |
| 5 | File Encryption CLI | ⬜ Planned | Command-line tool that encrypts/decrypts real files on disk |
| 6 | Attack Demos | ⬜ Planned | Demonstrations of cryptographic failure modes (tampering, weak KDF, nonce reuse) |

---

## Component Breakdown

### Phase 1 — Educational Cipher ✅

**Folder:** `phase-1-educational-cipher/`

Two implementations, built from Python's standard library only (zero installs):

- **`my_cipher.py`** — A Caesar cipher built from scratch. Encrypts `HELLO` → `KHOOR` by shifting each letter by a secret key, then reverses the process to decrypt. Includes a brute-force attacker that breaks the cipher by trying all 25 possible keys — proving why small keyspaces are unsafe.
- **`encrypt_decrypt.py`** — A more advanced stream cipher that maps every box in the ISC2 diagram to a function: PBKDF2 key derivation, salt + nonce as cryptovariables, keystream XOR as the algorithm, HMAC as the integrity tag.

**📷 See:** [`screenshots/phase-1-caesar-cipher-working.png`](screenshots/phase-1-caesar-cipher-working.png) and [`screenshots/phase-1-brute-force-attack.png`](screenshots/phase-1-brute-force-attack.png)

### Phase 2 — Real Crypto (AES) ✅

**Folder:** `phase-2-real-crypto/`

**`real_cipher.py`** — Re-implements the encrypt/decrypt pipeline using the `cryptography` library's Fernet (AES-128-CBC + HMAC-SHA256). Demonstrates:

- True 256-bit key generation (vs 25 keys in Phase 1)
- Automatic cryptovariables (salt + nonce) per encryption
- Built-in integrity protection — tampered ciphertext raises `InvalidToken`
- Wrong-key detection — also raises `InvalidToken` cleanly

The contrast with Phase 1 teaches **why "don't roll your own crypto" is a security rule**, not a stylistic preference.

**📷 See:** [`screenshots/phase-2-aes-encrypt-decrypt.png`](screenshots/phase-2-aes-encrypt-decrypt.png) and [`screenshots/phase-2-tamper-detection.png`](screenshots/phase-2-tamper-detection.png)

### File Integrity Monitor ✅

**Folder:** `file-integrity-monitor/`

**`fim.py`** — A working file integrity monitor — the same kind of tool Tripwire, OSSEC, and Wazuh use to detect intrusions on enterprise systems.

**How it works:**
1. **Baseline mode** (first run) — hashes the watched file with SHA-256 and saves the fingerprint as a trusted snapshot
2. **Check mode** (every run after) — re-hashes the file and compares to the saved baseline
3. **Alerts** if the fingerprint has changed (file was modified)

**Real-world threats this detects:**
- 🔴 Ransomware encryption (every file's hash changes)
- 🔴 Web defacement (`index.html` modification)
- 🔴 Backdoor injection into config files
- 🔴 Malware persistence (new files appearing where they shouldn't)

**Demonstrates the avalanche effect** — changing one byte produces a completely different fingerprint, which is what makes hash-based detection reliable.

**📷 See:** [`screenshots/fim-baseline-and-alert.png`](screenshots/fim-baseline-and-alert.png) — shows three runs: baseline created → OK status → ALERT after tampering

---

## Tools & Technologies

- **Language:** Python 3.13
- **Phase 1:** standard library only (`hashlib`, `hmac`, `secrets`, `base64`)
- **Phase 2:** `cryptography` library (Fernet / AES-128-CBC + HMAC-SHA256)
- **FIM:** `hashlib` (SHA-256), `os`, `json`
- **Concepts demonstrated:** symmetric encryption, key derivation (PBKDF2), HMAC integrity, cryptovariables (salt/nonce), avalanche effect, hash-based intrusion detection, baseline-and-compare detection logic

---

## Connection to ISC2 Certified in Cybersecurity

This lab is the practical companion to **CC Domain 5: Security Operations** (Hashing & Encryption):

- **Confidentiality** — the encryption algorithm hides the message (Phases 1 + 2)
- **Integrity** — the HMAC tag proves the message wasn't altered (Phase 2)
- **Key management** — turning a human password into algorithm-grade key material (Phase 1's PBKDF2 implementation)
- **Hashing** — one-way fingerprints used to detect tampering (FIM)
- **Why vetted crypto matters** — the build/break/secure arc proves it concretely

---

## How to Run

```bash
# Phase 1 — Caesar cipher (no installs needed)
python phase-1-educational-cipher/my_cipher.py

# Phase 2 — real AES (requires: pip install cryptography)
python phase-2-real-crypto/real_cipher.py

# File Integrity Monitor (no installs needed)
python file-integrity-monitor/fim.py
```

---

## Lessons Learned

- **Encryption hides; hashing detects.** They look similar (both use cryptographic primitives) but solve opposite problems — one is reversible by design, the other is one-way by design.
- **Keyspace is everything.** Caesar cipher's 25 keys vs AES-256's 2²⁵⁶ keys is the difference between "broken in a second" and "uncrackable in the lifetime of the universe."
- **Integrity ≠ Confidentiality.** AES alone hides the message but doesn't prove it wasn't tampered with. That's why Fernet bundles AES with HMAC by default.
- **Vetted libraries exist for a reason.** Even my hand-rolled stream cipher in Phase 1 is shorter and simpler than AES — and would still be unsafe in production. Real crypto libraries are the result of decades of cryptanalysis.
- **The "baseline and compare" pattern is everywhere in SOC work.** The FIM is the simplest example, but the same logic underlies SIEM rules, EDR behavior baselines, and anomaly detection.

---

*Last updated: 2026-05-15. Phase 1, Phase 2, and FIM v1 complete.*
