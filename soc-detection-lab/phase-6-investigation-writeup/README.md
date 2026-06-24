# Phase 6 — Incident Investigation Write-up

> A SOC analyst's real deliverable isn't an alert — it's a clear, defensible write-up of what happened and what to do about it. This is the brute-force from [Phase 4](../phase-4-first-detection/), documented the way a Tier-1 analyst would write a ticket.

---

## 🎫 Incident Report — RDP Brute-Force Attempt

| Field | Value |
|---|---|
| **Ticket ID** | SOC-LAB-0001 |
| **Severity** | High (Wazuh rule level 10) |
| **Status** | Closed — contained (lab) |
| **Analyst** | Olayinka Abimbowo |
| **Detection source** | Wazuh SIEM |
| **MITRE ATT&CK** | [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/) (Credential Access) |

---

## 1. Summary
The Wazuh SIEM detected a **brute-force authentication attack** against the Windows 11 endpoint `DESKTOP-2RCF6KO` (`192.168.56.102`). A single source host, **`192.168.56.104`**, made a rapid burst of failed RDP logon attempts against the local account **`WinUser`**. Wazuh correlated the individual failures into a high-severity **"Multiple Windows Logon Failures"** alert (rule `60204`) and classified the activity as **MITRE ATT&CK T1110**.

---

## 2. Timeline (UTC, lab time)

| Time | Event |
|---|---|
| T+0 | Remote Desktop (3389) exposed on the victim |
| T+~1m | Burst of failed logons begins from `192.168.56.104` against `WinUser` |
| T+~1m | Individual failures logged (Event ID **4625**, Wazuh rule `60122`) |
| T+~1m | Wazuh fires correlation alert (rule `60204`, level 10) |
| T+~2m | Authentication-failure counter rises **2 → 17**; MITRE chart shows **Brute Force** |

---

## 3. Evidence

**Detection (Wazuh):**
- Authentication failure events: spike to **17** in the window
- Rule `60122` — *Logon failure – unknown user or bad password* (per-attempt, level 5)
- Rule `60204` — *Multiple Windows Logon Failures* (correlation, **level 10**)
- MITRE mapping: **T1110 — Brute Force**, plus **T1110.001 — Password Guessing**

**Underlying log (Windows):**
- Event ID **4625** — *An account failed to log on*
- `targetUserName = WinUser`
- `logonType = 3 / 10` (network / remote-interactive — consistent with RDP)
- `ipAddress = 192.168.56.104`

**Attribution (analyst visualization):**
- Source-IP breakdown of failed logons: **`192.168.56.104` ≈ 11 events** (hostile), `127.0.0.1` ≈ 3 (benign/local)
- 📸 `../screenshots/phase-4-source-ip-attribution.png`

---

## 4. Analysis
The pattern is unambiguous: **many authentication failures in seconds, against one account, from one source, over RDP.** That signature does not match a user mistyping a password (which is sporadic and low-volume) — it matches an automated **password-guessing tool**. The targeted service (RDP/3389) and the burst rate confirm an external brute-force attempt rather than benign noise.

**Was the attack successful?** No. No corresponding **Event ID 4624 (successful logon)** from `192.168.56.104` was observed during or immediately after the failure burst. The account was **not** compromised. (Had any of the sprayed passwords matched, Hydra would have reported a success and a 4624 would appear — the absence of both confirms containment.)

**Triage verdict:** **True Positive — confirmed brute-force attempt, unsuccessful.**

---

## 5. Impact
- **Confidentiality / Integrity / Availability:** No impact. No successful authentication; no access gained.
- **Exposure:** The victim had RDP intentionally exposed for this exercise. In production, an internet-exposed RDP service is a critical risk regardless of outcome.

---

## 6. Recommended Response (what an analyst would action)
1. **Block the source IP** `192.168.56.104` at the firewall.
2. **Restrict RDP** — remove internet exposure; require a VPN/jump host; restrict by source IP.
3. **Enforce account lockout** (e.g. 5 failures → 15-min lockout) to throttle guessing.
4. **Require strong passwords + MFA** on remote-access accounts.
5. **Enable Network Level Authentication (NLA)** for RDP (already on in this case).
6. **Add a detection/alert** for repeated 4625s per source IP (already firing as rule `60204`).

---

## 7. Detection Engineering Notes
- The out-of-the-box Wazuh ruleset (`60122` → `60204` correlation) caught this with **no custom rule required**.
- **Gap identified in Phase 4:** the earlier Nmap recon was **not** detected (firewall dropped probes; Windows doesn't log dropped packets). A network IDS (Suricata) would close this gap — a planned enhancement.
- **Next step ([Phase 5](../phase-5-custom-rules/)):** author a custom Wazuh rule to tune brute-force thresholds and enrich the alert.

---

## 🧠 Skills demonstrated in this write-up
Alert triage · log analysis (Windows 4625/4624) · MITRE ATT&CK mapping · attack attribution · impact assessment · incident documentation · actionable remediation — the core deliverables of a Tier-1 SOC analyst.
