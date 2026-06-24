# Cybersecurity Home Lab

> **Self-directed cybersecurity projects. Building, breaking, and securing real systems.**

By **Olayinka Abimbowo** — aspiring Junior SOC Analyst (Canada).

This repository is my personal home lab. Every project here is something I built on my own initiative — not coursework, not a tutorial follow-along. Each one demonstrates a hands-on cybersecurity skill with working code, real attack scenarios, and detection logic that mirrors what a SOC analyst does day-to-day.

If you're a recruiter or hiring manager: **this repo shows what I do when nobody tells me what to build.** My structured coursework lives in [Cybersecurity-Portfolio](https://github.com/Halo-hub501/Cybersecurity-Portfolio).

---

## 🧪 Projects

### 🔐 [Crypto Lab](crypto-lab/) — Encryption, Integrity, and Detection from the Ground Up

A hands-on cryptography lab that **builds, breaks, then properly secures** an encrypt/decrypt system, then extends it into a real SOC detection tool.

- **Phase 1** ✅ Caesar cipher built from scratch + brute-force attack proving why small keyspaces are unsafe
- **Phase 2** ✅ Real AES via the `cryptography` library with tamper detection and wrong-key handling
- **File Integrity Monitor** ✅ Working SHA-256 based detection tool — same baseline-and-compare logic as Tripwire / OSSEC / Wazuh
- **Up next:** FIM v2 (whole-folder monitoring), file encryption CLI, attack demos

**Skills demonstrated:** Python 3, symmetric encryption (AES), key derivation (PBKDF2), HMAC integrity, SHA-256 hashing, hash-based intrusion detection, the build/break/secure mindset.

**Tied to:** ISC2 Certified in Cybersecurity — Domain 5 (Security Operations: Hashing & Encryption).

→ **[See full writeup, code, and screenshots](crypto-lab/)**

---

### 🛡️ [SOC Detection Lab](soc-detection-lab/) — A Working SIEM, Real Attacks, Custom Detection Rules

A self-built **purple-team environment**: Kali attacker, Windows 11 endpoint with Sysmon, and a Wazuh SIEM — all running on an isolated host-only network. I run real attacks and investigate the detections they trigger.

- **Phase 1** ✅ Lab foundation — three VMs (Ubuntu, Windows 11, Kali) on an isolated network in VirtualBox
- **Phase 2** ✅ Wazuh SIEM stand-up, hardening, and air-gap verification
- **Phase 3** ✅ Wazuh agent + Sysmon shipping endpoint telemetry to the SIEM
- **Phase 4** ✅ First detection — Nmap recon (a real detection gap) + Hydra RDP brute-force → **MITRE T1110** alert → source-IP attribution
- **Phase 5** ⏳ Custom Wazuh detection rules + false-positive tuning
- **Phase 6** ✅ Analyst-style incident writeup of the brute-force (summary, timeline, evidence, impact, response)

**Skills demonstrated:** SIEM operations (Wazuh), endpoint telemetry (Sysmon), detection engineering, MITRE ATT&CK mapping, adversary emulation (Nmap, Hydra), Windows event-log investigation & attack attribution, VM/network isolation, incident documentation.

**Tied to:** Google Cybersecurity Certificate — Module 6 (Detection & Response); ISC2 CC Domain 5 (Security Operations).

→ **[Explore the lab — architecture and all phase walkthroughs](soc-detection-lab/)**

---

## 💡 Why "Home Lab"?

Most entry-level cybersecurity candidates have the same résumé: a few certificates, some Coursera assignments, maybe a TryHackMe room. That's table stakes — it doesn't differentiate.

**A home lab is what differentiates.** It shows:
- I learn outside the classroom
- I can plan and execute multi-phase technical projects
- I think like an attacker AND a defender
- I document my work the way an analyst would document an investigation
- I build things that *actually run* — not just slides and theory

These are exactly the skills a SOC team needs in someone they hire entry-level.

---

## 🎯 Background

**Aspiring Junior SOC Analyst.** Currently completing the Google Cybersecurity Professional Certificate (Module 6 of 8) and the ISC2 Certified in Cybersecurity course (4 of 5 domains complete). Based in Canada, actively building toward landing my first role in a Security Operations Center.

**Connect:** Open to entry-level SOC Analyst, Security Analyst, or Cybersecurity Analyst opportunities.

---

*This repo is actively growing — new projects and phases ship regularly. Star ⭐ to follow along.*
