# Phase 3 — Endpoint Telemetry

> **Goal:** Install the Wazuh agent on the Windows 11 victim so it ships logs to the SIEM, and confirm that real endpoint activity — Windows security events and Sysmon telemetry — streams into the Security Events page.

By the end of Phase 2 the SIEM was watching only *itself* (agent `000`, the manager's own host). That's a SIEM with nothing to defend. Phase 3 is where the lab becomes real: a separate endpoint starts reporting in, and "0 agents" becomes "1 active agent."

---

## 🧠 Concepts before commands

### 1. What a Wazuh agent actually is
The **agent** is a lightweight service installed on an endpoint (Windows/Linux/Mac). It reads the machine's logs locally and forwards them to the manager. In a real SOC, deploying agents *is* onboarding — every protected machine has one, and the agent fleet is your visibility.

### 2. The two ports that matter
The agent talks to the manager over the **host-only network** on two ports:

| Port | Purpose |
|---|---|
| **1515** | One-time **enrollment** (registers the agent with the manager) |
| **1514** | Ongoing **log traffic** |

Neither needs the internet — agent ↔ manager traffic rides the isolated `192.168.56.0/24` lab network. The *only* thing that touches the internet is downloading the agent installer (~10 MB), and we close that hole afterward.

### 3. Sysmon — the reason this endpoint is worth monitoring
**Sysmon** (System Monitor, a Sysinternals tool) was installed back in Phase 1 with the **SwiftOnSecurity config**. It logs deep detail Windows doesn't by default — process creation with command lines and hashes, network connections, file/registry changes — to `Applications and Services Logs/Microsoft/Windows/Sysmon/Operational`. The Wazuh agent picks that channel up and forwards it, so the SIEM gets *rich* telemetry, not just basic logons.

### 4. Version matching
The agent **major version must match the manager** (here both **4.7.x**). A mismatched agent can enroll but fail to communicate properly. The dashboard's deploy wizard auto-generates a command for the right version — use what it gives you.

---

## 🛠️ Step-by-step (what was actually done)

### Step 1 — Generate the deploy command
On the dashboard: **☰ → Agents → Deploy new agent**. Select:
- **OS:** Windows (MSI 32/64-bit)
- **Server address:** `192.168.56.103` (the manager's **host-only** IP — this is the field people get wrong; anything else and the agent installs but never connects)

The wizard prints an `msiexec` install command.

### Step 2 — Install the agent on the victim (silently)
The install **must** run silently with the `WAZUH_MANAGER` property baked in. The command that worked, run in an **Administrator PowerShell** on the victim:

```powershell
cd C:\Users\WinUser\Downloads
msiexec /i wazuh-agent-4.7.5-1.msi /q WAZUH_MANAGER=192.168.56.103 WAZUH_AGENT_NAME=Victim-win11
```

> `/q` = quiet/silent. `WAZUH_MANAGER` tells the agent where the SIEM is. Without `WAZUH_AGENT_NAME` the agent falls back to the **Windows hostname** as its name (see gotchas).

### Step 3 — Start the service
The MSI registers the service but leaves it **stopped**. Start it explicitly:

```powershell
Start-Service WazuhSvc      # or:  NET START WazuhSvc
Get-Service WazuhSvc        # confirm Status = Running
```

### Step 4 — Verify it connected
On the dashboard: **☰ → Agents**. The endpoint appears as **Active** 🟢 with 100% coverage:

| Field | Value |
|---|---|
| ID | `001` |
| Name | `DESKTOP-2RCF6KO` (the Windows hostname) |
| IP | `192.168.56.102` |
| OS | Microsoft Windows 11 Enterprise Evaluation |
| Version | `v4.7.5` (matches the manager ✅) |
| Status | **active** 🟢 |

**Event volume jumped from ~19 to ~450** the moment the agent connected — that spike *is* the victim's telemetry flowing in.

### Step 5 — Re-isolate the victim
The NAT adapter (used only for the installer download) was **disabled again** in VirtualBox → Settings → Network → Adapter 2. The agent reconnects over host-only, so it stays Active — but the victim now has **no internet path**, which is the posture we want before running attacks.

---

## 🧯 Gotchas hit during this phase (documented so they don't bite twice)

- **No Guest Additions → no shared clipboard.** Host copy/paste does not reach the VM, so every command had to be typed by hand. (Installing VirtualBox Guest Additions would fix this for future work.)
- **Host vs. VM confusion.** The agent installer and `msiexec` were accidentally run on the **host laptop** first (host user `Halo`) instead of *inside* the VM (user `WinUser`). The fix is to always confirm the window title reads **"Victim-win11 [Running] – Oracle VirtualBox"** and the prompt shows `C:\Users\WinUser>` before typing. *Everything for the agent must happen inside the VM.*
- **`msiexec` syntax is unforgiving.** Failures came from `\User\` vs `\Users\`, `misiexec` typos, and a **missing space** before `/q` / `WAZUH_MANAGER`. Each made the install fail silently, so `NET START WazuhSvc` then reported *"service name is invalid."*
- **Double-clicking the MSI launches the GUI installer**, which has **no field for the manager IP** — it installs an agent that can't phone home. Always install from the command line with the `WAZUH_MANAGER` property.
- **Chrome flags the download** ("Insecure download blocked") because the MSI is served over HTTP from `packages.wazuh.com`. It's the legitimate vendor package — click **Keep**. (Good triage lesson: *insecure transport ≠ malicious file.*)
- **Agent name defaults to the hostname.** The winning command omitted `WAZUH_AGENT_NAME`, so the agent registered as `DESKTOP-2RCF6KO` instead of `Victim-win11`. Set the name explicitly at install time — it can't be changed after enrollment.

---

## ✅ Phase 3 "done" looks like
- [x] Wazuh agent **v4.7.5** installed on the Windows 11 victim
- [x] Service running; agent shows **Active** with 100% coverage in the dashboard
- [x] Event volume increased sharply (≈19 → ≈450) once connected
- [x] Sysmon telemetry confirmed flowing (process/network/file events visible)
- [x] Victim **re-isolated** (NAT disabled) — monitored but air-gapped

---

## 🖼️ Screenshots
_Add these to `../screenshots/`:_
- `phase-3-agent-active.png` — Agents page showing `DESKTOP-2RCF6KO` Active, v4.7.5, IP 192.168.56.102
- `phase-3-inventory.png` — agent Inventory data (hardware + open ports mapped to processes)

---

## ➡️ Next
**[Phase 4 — First Detection](../phase-4-first-detection/):** launch a real attack from Kali and watch the SIEM catch it.
