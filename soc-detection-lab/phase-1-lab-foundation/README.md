# Phase 1 — Lab Foundation

> **Goal:** Build three VMs (Ubuntu, Windows 10, Kali) on an isolated network in VirtualBox, and prove they can talk to each other but cannot escape to the public internet during attack scenarios.

This phase is **not glamorous** — there are no alerts, no attacks, no SIEM yet. But everything that comes after depends on this being done correctly. A messy lab foundation is how people accidentally infect their own home network with the malware they were "just experimenting with."

---

## 🧠 Concepts before commands

### 1. What is a hypervisor?

A **hypervisor** is software that lets one physical machine pretend to be many. Each pretend machine is a **virtual machine (VM)** — a full operating system running inside a window on your host. From the VM's perspective, it has its own CPU, RAM, disk, and network card. In reality those are all slices of your real hardware that the hypervisor hands out.

We're using **VirtualBox** because it's free, runs on Windows, and doesn't need anything fancy. (VMware Workstation Pro is now free too — it's slightly faster, but VirtualBox is the standard for SOC lab tutorials and the one most employers will recognize on a resume.)

### 2. Why three VMs and not two?

You need three because each one has a job that conflicts with the others:

| VM | Role | Why it can't share a box with the others |
|---|---|---|
| **Ubuntu (Wazuh server)** | The SIEM — collects and analyzes logs | If the attacker compromises this, your "logs" are no longer trustworthy. The SIEM has to live somewhere the attacker can't reach. |
| **Windows 10 (victim)** | The endpoint being attacked | This VM gets malware run on it deliberately. It needs to be disposable. |
| **Kali Linux (attacker)** | Where you run offensive tools | Kali ships with tools that can hurt your real network if it's not isolated. Keeping it on its own VM means you can pull its network cable (virtually) the moment something looks wrong. |

### 3. What is host-only networking and why we use it

VirtualBox gives you several networking modes. The two that matter for us:

- **NAT** — the VM can reach the internet through your host's connection, but nothing on the internet can reach the VM. This is the *default* and it's fine for installing updates.
- **Host-only** — the VM can talk to your host and to other VMs on the same host-only network, but **cannot reach the internet at all**. This is the mode we use for lab isolation.

We give each VM **two network adapters**:
- **Adapter 1 (host-only)** — always on. This is the "lab network." All three VMs talk to each other on this one.
- **Adapter 2 (NAT)** — turned ON only when we need to download/update something. Turned OFF before we run any attacks.

That second adapter is your air gap. When NAT is off, malware running on the Windows VM has nowhere to phone home, even if it tries.

---

## 🧰 What you'll download

| Software | Purpose | Where |
|---|---|---|
| **VirtualBox** + Extension Pack | The hypervisor | https://www.virtualbox.org/wiki/Downloads |
| **Ubuntu Server 22.04 LTS** ISO | OS for the Wazuh SIEM VM | https://ubuntu.com/download/server |
| **Windows 10 Enterprise Eval** ISO | OS for the victim VM (90-day eval, free, legitimate) | https://www.microsoft.com/en-us/evalcenter |
| **Kali Linux** ISO (Installer, not Live) | OS for the attacker VM | https://www.kali.org/get-kali/#kali-installer-images |

> ⚠️ Save all ISOs somewhere you'll remember. I use `C:\VMs\ISOs\`. Each ISO is between 2 and 5 GB — total around 12 GB of downloads.

---

## 📐 VM sizing on a 32 GB host

You have 32 GB of RAM and presumably ~250 GB of free disk. Here's the allocation:

| VM | vCPU | RAM | Disk (dynamic) | Why |
|---|---|---|---|---|
| Ubuntu (Wazuh) | 2 | 4 GB | 50 GB | Wazuh's minimum is 4 GB. Logs eat disk over time — leave 50 GB so we don't run out at Phase 4. |
| Windows 10 victim | 2 | 4 GB | 60 GB | Windows is bloated. 4 GB is the floor for it to feel usable. 60 GB so it has room for sysmon logs + tools. |
| Kali attacker | 2 | 4 GB | 40 GB | Kali is lean. 4 GB is comfortable. 40 GB covers wordlists + tools. |
| **Lab total** | **6 vCPU** | **12 GB** | **150 GB** | |
| **Your host keeps** | rest | **20 GB** | rest | Plenty for browser, IDE, and not making your fan scream. |

"Dynamic" disk means VirtualBox only uses the space you actually fill — a 60 GB dynamic disk doesn't take 60 GB on day one. Don't worry about the disk numbers feeling big.

---

## 🛠️ Step-by-step

### Step 1 — Install VirtualBox + Extension Pack

1. Download and install VirtualBox.
2. Download the **Extension Pack** (same page). Open VirtualBox → File → Tools → Extension Pack Manager → Install. The extension pack adds USB 2/3 support and the encryption you may want for snapshots later.

### Step 2 — Create the host-only network

This is the lab network all three VMs will share.

1. Open VirtualBox → **File → Tools → Network Manager → Host-only Networks**.
2. Click **Create**. A network appears, usually named `VirtualBox Host-Only Ethernet Adapter`.
3. Select it and check:
   - **IPv4 address:** `192.168.56.1` (this is the host's address on the lab network)
   - **IPv4 mask:** `255.255.255.0`
   - **DHCP server:** ✅ enabled, range `192.168.56.100 – 192.168.56.200`
4. Apply.

You now have a virtual switch the three VMs will plug into.

### Step 3 — Create the Ubuntu (Wazuh) VM

1. VirtualBox → **New**.
2. Name: `wazuh-server`. Type: Linux. Version: Ubuntu (64-bit).
3. RAM: **4096 MB**. CPU: **2 cores**. Disk: **50 GB dynamic VDI**.
4. Once the VM is created but BEFORE first boot:
   - **Settings → Network → Adapter 1**: Attached to **Host-only Adapter**, name = the one you created above.
   - **Settings → Network → Adapter 2**: Attached to **NAT**, ✅ Enabled. (We'll use this only during install.)
   - **Settings → Storage**: attach the Ubuntu Server ISO to the optical drive.
5. Start the VM. Install Ubuntu Server (defaults are fine — install OpenSSH server when prompted, you'll want it for Phase 2).
6. After install, log in and run `sudo apt update && sudo apt upgrade -y`.
7. Once updated: shut down. Reopen Settings → Network → **disable Adapter 2 (NAT)**. The VM is now lab-isolated.

### Step 4 — Create the Windows 10 victim VM

1. VirtualBox → **New**.
2. Name: `victim-win10`. Type: Microsoft Windows. Version: Windows 10 (64-bit).
3. RAM: **4096 MB**. CPU: **2 cores**. Disk: **60 GB dynamic VDI**.
4. Same network setup as before: Adapter 1 = host-only, Adapter 2 = NAT (enabled for install only).
5. Attach the Windows 10 ISO. Start the VM. Install Windows (Enterprise Eval — accept the 90-day trial).
6. Once installed, install **VirtualBox Guest Additions** (Devices menu → Insert Guest Additions CD). This gives you copy/paste and a usable screen resolution.
7. Update Windows fully. Then **disable Adapter 2 (NAT)**.

### Step 5 — Create the Kali attacker VM

1. VirtualBox → **New**.
2. Name: `kali-attacker`. Type: Linux. Version: Debian (64-bit).
3. RAM: **4096 MB**. CPU: **2 cores**. Disk: **40 GB dynamic VDI**.
4. Same network setup: Adapter 1 = host-only, Adapter 2 = NAT (enabled for install only).
5. Attach the Kali ISO. Start the VM. Run the installer (defaults are fine, create a non-root user).
6. After install, run `sudo apt update && sudo apt full-upgrade -y`.
7. **Disable Adapter 2 (NAT)**.

### Step 6 — Verify connectivity

This is the "done" check for Phase 1. From inside each VM, find its IP address (it should be in `192.168.56.x`):

- **Ubuntu / Kali:** `ip addr` — look for the interface with a `192.168.56.x` address
- **Windows:** `ipconfig` in PowerShell — same thing

Now from each VM, ping the other two by IP. For example, if Wazuh is `192.168.56.101`, Windows is `192.168.56.102`, Kali is `192.168.56.103`:

```bash
# from Kali
ping 192.168.56.101    # should reply (Wazuh)
ping 192.168.56.102    # should reply (Windows — you may need to allow ICMP in Windows Firewall)
ping 8.8.8.8           # should TIME OUT — this proves NAT is off and the lab is isolated
```

> 🔧 If Windows doesn't reply to ping: open Windows Defender Firewall → Advanced Settings → Inbound Rules → enable "File and Printer Sharing (Echo Request - ICMPv4-In)" for the Private profile. Windows blocks ICMP by default.

---

## ✅ Phase 1 "done" looks like

- [ ] VirtualBox installed with the Extension Pack
- [ ] Host-only network `192.168.56.0/24` exists with DHCP enabled
- [ ] Ubuntu, Windows 10, and Kali all installed and fully updated
- [ ] Each VM has Adapter 1 on the host-only network and Adapter 2 (NAT) **disabled**
- [ ] Each VM can ping the other two
- [ ] None of the VMs can ping `8.8.8.8` (proves isolation)

**Take a screenshot of the three terminals/PowerShell windows side by side showing successful inter-VM pings and a timed-out `ping 8.8.8.8`.** That's the artifact for this phase. Drop it in this phase folder as `phase-1-isolation-proof.png`.

---

## 🧯 Common things that go wrong

- **"I can't ping the Windows VM from Kali."** Windows Firewall blocks ICMP by default. Enable the inbound ICMPv4 rule (see the note in Step 6).
- **VMs got IPs in `10.0.x.x` instead of `192.168.56.x`.** You left Adapter 1 set to NAT instead of host-only. Shut the VM down, fix the adapter, restart.
- **Wazuh VM feels sluggish during install.** Wazuh's *running* memory floor is 4 GB but the Ubuntu *installer* is fine at less. Keep it at 4 GB; we'll need every byte once Wazuh is running.
- **"I forgot to disable the NAT adapter on one VM."** That VM is no longer isolated. Shut it down, disable Adapter 2, restart. Don't run any attacks while NAT is on, on any VM.

---

## ➡️ When this phase is done

Drop the screenshot in this phase folder and we'll move to **Phase 2 — SIEM Stand-up**: installing Wazuh on the Ubuntu VM and getting the dashboard online.
