# Phase 2 — SIEM Stand-up

> **Goal:** Install Wazuh on the Ubuntu VM, get the dashboard online from the host browser, and tour the parts of the platform a SOC analyst actually uses — agents, security events, decoders, and rules.

By the end of this phase you have a working SIEM with **zero agents reporting**. That's intentional. Before connecting endpoints in Phase 3, you need to know what you're looking at. Most "I have a SIEM" tutorials skip the tour and dump you straight into chasing alerts you don't understand.

---

## 🧠 Concepts before commands

### 1. What a SIEM actually is

**SIEM = Security Information and Event Management.** Strip the marketing off and it's three things stapled together:

1. **A log pipeline.** Endpoints, firewalls, cloud services, anything that produces a log — it all ships into one place.
2. **A parser + rules engine.** Raw logs are unreadable. The SIEM normalizes them into structured fields ("this is a Windows 4624 logon, user = `alice`, source IP = `10.0.0.5`") and then runs rules against those fields to decide what's worth alerting on.
3. **A search + dashboard layer.** So a human (you) can query "show me every failed login in the last hour" without grepping raw files on 200 machines.

A SOC analyst spends most of their day in layer 3 — searching, triaging, and pivoting on alerts that layer 2 generated from logs that layer 1 collected.

### 2. Why Wazuh

Wazuh is **free, open-source, runs on a single VM, and ships with hundreds of detection rules out of the box** (MITRE ATT&CK mapped). It's also one of the few SIEMs that mid-market companies actually deploy in production, so the skills transfer. Splunk is the industry heavyweight but it's pay-to-play; Elastic Security is good but heavier to stand up. Wazuh is the right fit for a lab and a resume bullet.

### 3. Wazuh has three components — all going on one VM

A production Wazuh deployment usually splits these onto separate servers. For a lab they all live on the same Ubuntu VM, installed by a single script:

| Component | What it does |
|---|---|
| **Wazuh Manager** | The brain. Receives logs from agents, runs them through decoders and rules, generates alerts. |
| **Wazuh Indexer** | A fork of OpenSearch. Stores the alerts and parsed events so they're searchable. |
| **Wazuh Dashboard** | The web UI. A fork of OpenSearch Dashboards. This is what you'll have open in your browser all day. |

You won't have to think about these as separate things much — but when something breaks, knowing which of the three is broken cuts your debugging time in half.

### 4. The terms you'll see everywhere

- **Decoder** — the thing that takes a raw log line and turns it into structured fields. There's a decoder for sshd, one for Sysmon, one for Apache, etc.
- **Rule** — the thing that fires an alert based on those fields. Rules have a **level** (0–15). Level 0 = informational, level 12+ = alert-worthy, level 15 = "wake someone up."
- **Agent** — a small piece of software you install on an endpoint (Windows, Linux, Mac) that ships logs to the manager. We install our first agent in Phase 3.

---

## ✅ Pre-flight checks

Before installing anything, confirm:

- [ ] Phase 1 is done — Ubuntu VM exists, host-only IP in `192.168.56.x`, can ping from host
- [ ] Ubuntu VM has **at least 4 GB RAM** assigned (Wazuh's hard floor — it will fail to start below this)
- [ ] You temporarily re-enable **Adapter 2 (NAT)** on the Ubuntu VM for the install — the installer downloads ~1 GB of packages from the internet
- [ ] You have a terminal open to the Ubuntu VM (either the VirtualBox console window or SSH from your host)

> 🔧 Reminder: the moment the install finishes, **disable NAT again**. The SIEM does not need internet access during attack scenarios.

---

## 🛠️ Step-by-step

### Step 1 — SSH into the Ubuntu VM from your host

Working in the VirtualBox console window gets old fast (no copy/paste, fixed window size). SSH from PowerShell instead:

```powershell
ssh youruser@192.168.56.101    # replace with your actual Ubuntu IP
```

If it complains about the host key, that's expected on first connect — type `yes`.

### Step 2 — Run the Wazuh all-in-one installer

Wazuh ships an official script that installs the manager, indexer, and dashboard in one go. From the Ubuntu shell:

```bash
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

The `-a` flag means "all-in-one — install everything on this single host with the default config." The install takes **10–20 minutes** depending on disk and network speed.

When it finishes, the script prints a block that looks like this — **copy it somewhere safe**, you'll need the admin password:

```
INFO: --- Summary ---
INFO: You can access the web interface https://<wazuh-server-ip>
    User: admin
    Password: <some-generated-password>
```

> 🔒 The password is generated and shown only once. If you lose it, you can recover it from `/etc/wazuh-indexer/wazuh-passwords.tool.sh` — but easier to just save it now.

### Step 3 — Confirm the three services are running

```bash
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
```

All three should show `active (running)` in green. If any is `failed`, jump to the troubleshooting section.

### Step 4 — Open the dashboard from your host browser

On your **Windows host**, open a browser and go to:

```
https://192.168.56.101    # your Ubuntu VM's IP
```

You will get a **certificate warning** — that's expected. Wazuh ships with self-signed certs for the lab. Click through it (Advanced → Proceed). In production you'd swap these for real certs; for a lab, self-signed is fine.

Log in with `admin` + the password from Step 2.

### Step 5 — Disable NAT, take a screenshot

1. Shut down the Ubuntu VM.
2. VirtualBox → Settings → Network → **disable Adapter 2 (NAT)**.
3. Boot Ubuntu back up.
4. Reload `https://192.168.56.101` from your host browser — it should still load (host-only traffic doesn't need NAT).
5. **Screenshot the Wazuh dashboard home page** showing 0 agents connected. Save as `../screenshots/phase-2-wazuh-dashboard.png`.

---

## 🔍 The 10-minute dashboard tour

Spend ten minutes clicking around before you touch Phase 3. Here's what to find and why it matters:

| Where | What you're looking at | Why a SOC analyst cares |
|---|---|---|
| **☰ → Agents** | List of endpoints reporting in (empty for now) | This is your fleet view. In a real SOC this might have 5,000 rows. |
| **☰ → Security events** | Search and timeline of all alerts | This is the page you'd live in during a shift. Empty for now — nothing's attacking us yet. |
| **☰ → Threat Hunting** | Pre-built dashboards (MITRE ATT&CK, suspicious processes, etc.) | Where you hunt without an alert telling you what to look at. |
| **☰ → Management → Rules** | Every detection rule on the manager (thousands shipped by default) | This is what generates alerts. We add custom rules here in Phase 5. |
| **☰ → Management → Decoders** | Every log parser the manager knows | If a log shows up but no rule fires, the decoder is usually why. |
| **☰ → Management → Configuration** | `ossec.conf` viewer | The manager's master config. Read-only here; edited via SSH. |

> 💡 Bookmark the **Security events** page. That's the analyst's default view and you'll come back to it constantly.

---

## ✅ Phase 2 "done" looks like

- [ ] `wazuh-install.sh -a` ran to completion without errors
- [ ] All three services (`wazuh-manager`, `wazuh-indexer`, `wazuh-dashboard`) are `active (running)`
- [ ] You can hit `https://<ubuntu-ip>` from your host browser and log in as `admin`
- [ ] Ubuntu VM's NAT adapter is **disabled** again — lab is isolated
- [ ] Screenshot of the dashboard home (0 agents) saved as `screenshots/phase-2-wazuh-dashboard.png`
- [ ] You've clicked through Agents, Security events, Rules, and Decoders so the layout isn't a mystery in Phase 3

---

## 🧯 Common things that go wrong

- **Installer fails partway through with a 4xx/5xx from `packages.wazuh.com`.** You probably never re-enabled NAT on the Ubuntu VM. Re-enable Adapter 2, `sudo bash ./wazuh-install.sh -a` again. The script is safe to re-run.
- **`wazuh-indexer` keeps restarting / `failed`.** Almost always not enough RAM. Bump the VM to 4 GB (or higher), restart the VM, then `sudo systemctl restart wazuh-indexer`. Check with `sudo journalctl -u wazuh-indexer -n 50`.
- **Browser can reach `https://192.168.56.101` but the page hangs forever.** `wazuh-dashboard` takes 60–90 seconds to fully start after a reboot. Give it a minute, then refresh. If it's still down: `sudo systemctl restart wazuh-dashboard`.
- **"I lost the admin password."** SSH to the Ubuntu VM and run `sudo /usr/share/wazuh-indexer/plugins/opensearch-security/tools/wazuh-passwords-tool.sh -au admin -ap NEWPASSWORDHERE`. (Use a strong password — even on a lab, build the habit.)
- **Cert warning every time you open the dashboard.** Expected. Self-signed certs. You can import the cert into your browser's trust store if it bothers you, but it's not required for the lab.

---

## ➡️ When this phase is done

Drop the dashboard screenshot in `screenshots/` and move to **Phase 3 — Endpoint Telemetry**: installing Sysmon and the Wazuh agent on the Windows 10 VM, and watching the first real events stream into the Security events page you just toured.
