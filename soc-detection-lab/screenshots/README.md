# 📸 Screenshots

This folder holds the visual proof for each phase. Drop your images here using the **exact filenames** below so the phase READMEs render them. Tip: for the cleanest look, use real screen captures (**Win + Shift + S** on the host) rather than phone photos where you can.

> You took many photos during the build — add as many as you like. The filenames below are the ones already referenced by the READMEs; extra images are welcome (just give them descriptive names and link them from the relevant phase README).

## Phase 1 — Lab Foundation
- `phase-1-vms-list.png` — VirtualBox Manager showing all 3 VMs (Kali, wazuh-server, Victim-win11)
- `phase-1-isolation-proof.png` — host-only network config / inter-VM connectivity

## Phase 2 — SIEM Stand-up
- `phase-2-wazuh-dashboard.png` — dashboard home, **0 agents** (clean SIEM)
- `phase-2-security-events.png` — Security Events page (agent 000 self-monitoring)
- `phase-2-ping-fail.png` — `ping 8.8.8.8` failing = internet air-gap verified
- `phase-2-mitre.png` — MITRE ATT&CK module
- `phase-2-status.png` — Management → Status (manager daemons)

## Phase 3 — Endpoint Telemetry
- `phase-3-agent-active.png` — Agents page: `DESKTOP-2RCF6KO` **Active**, v4.7.5, 192.168.56.102
- `phase-3-inventory.png` — agent Inventory data (hardware + open ports → processes)

## Phase 4 — First Detection
- `phase-4-nmap-scan.png` — Nmap recon result (all ports filtered)
- `phase-4-rdp-enabled.png` — RDP enabled / port 3389 listening on the victim
- `phase-4-hydra-attack.png` — Hydra brute-force running in Kali
- `phase-4-bruteforce-detection.png` — dashboard showing **Brute Force (T1110)** + auth-failure spike
- `phase-4-source-ip-attribution.png` — source-IP bar chart pinning the attack to `192.168.56.104`

## Phase 6 — Investigation Writeup
- Reuse the Phase 4 detection + attribution screenshots as evidence exhibits.
