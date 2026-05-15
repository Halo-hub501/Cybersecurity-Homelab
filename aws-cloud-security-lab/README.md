t# AWS Cloud-Native Security Lab

**A purple-team homelab demonstrating real AWS attack paths and the cloud-native detections that catch them.**

Built by Olayinka as a portfolio capstone for Junior SOC Analyst roles. This project goes beyond classroom exercises — every scenario is executed in a live AWS environment, with logs captured, detections written, and findings documented to mirror real SOC analyst work.

---

## Why This Lab Exists

Most entry-level cybersecurity candidates can talk about Wireshark, NIST CSF, and the CIA triad. Very few have **actually attacked and defended real cloud infrastructure**. This lab closes that gap by:

1. Running real attacks against intentionally vulnerable AWS resources
2. Capturing the telemetry those attacks generate (CloudTrail, VPC Flow Logs, GuardDuty findings)
3. Writing the detection logic a SOC analyst would use to spot them
4. Mapping each scenario to the MITRE ATT&CK Cloud Matrix

The goal isn't "I deployed AWS resources." The goal is **"I can think like an attacker AND a defender in a cloud environment."**

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AWS Account (Lab Tenant)                   │
│                                                             │
│   ┌─────────────────────────┐    ┌──────────────────────┐   │
│   │  Vulnerable Infrastructure │  │   Detection Stack    │   │
│   │  - Misconfigured IAM      │  │   - CloudTrail        │   │
│   │  - Public S3 buckets      │  │   - GuardDuty         │   │
│   │  - EC2 w/ IMDSv1 exposed  │  │   - AWS Config        │   │
│   │  - Vulnerable Lambda      │  │   - EventBridge rules │   │
│   │  - Over-permissioned keys │  │   - Security Hub      │   │
│   └─────────────────────────┘    └──────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
              ▲                              ▲
              │ Attacks                      │ Findings
       ┌──────┴────────┐             ┌──────┴────────┐
       │  Attacker     │             │  SOC Analyst  │
       │  (Pacu, AWS   │             │  (CloudTrail  │
       │   CLI, curl)  │             │   Insights,   │
       │               │             │   GuardDuty)  │
       └───────────────┘             └───────────────┘
```

---

## Phases

| # | Phase | Status | Deliverable |
|---|-------|--------|-------------|
| 1 | Foundation & Safety Setup | 🔄 In Progress | AWS account hardened, CLI configured, CloudTrail on |
| 2 | Vulnerable Infrastructure | ⬜ Upcoming | CloudGoat scenarios deployed + hand-rolled targets |
| 3 | Detection Stack | ⬜ Upcoming | GuardDuty, Config rules, EventBridge alerts wired up |
| 4 | Attack & Detect Scenarios | ⬜ Upcoming | 8-10 paired writeups w/ evidence and MITRE mapping |
| 5 | Portfolio Polish | ⬜ Upcoming | Final README, diagrams, demo video (optional) |

---

## Planned Attack Scenarios

| # | Scenario | MITRE ATT&CK | Detection Source |
|---|----------|--------------|------------------|
| 1 | IAM enumeration with stolen access key | T1087.004 (Account Discovery: Cloud) | CloudTrail + GuardDuty |
| 2 | S3 bucket misconfiguration → data exfiltration | T1530 (Data from Cloud Storage) | S3 access logs + Config |
| 3 | IMDSv1 abuse → role credential theft | T1552.005 (Unsecured Credentials: Cloud Instance Metadata) | VPC Flow + CloudTrail |
| 4 | IAM privilege escalation via PassRole | T1098 (Account Manipulation) | CloudTrail + IAM Access Analyzer |
| 5 | Lambda function abuse for persistence | T1546 (Event Triggered Execution) | CloudTrail + CloudWatch |
| 6 | Public AMI / snapshot exposure | T1580 (Cloud Infrastructure Discovery) | Config + Security Hub |
| 7 | CloudTrail tampering / logging disable | T1562.008 (Disable Cloud Logs) | CloudTrail (recursive) + GuardDuty |
| 8 | Cross-account role assumption abuse | T1078.004 (Valid Accounts: Cloud) | CloudTrail + Access Analyzer |

---

## Tools & Technologies

**AWS Services:** IAM, S3, EC2, Lambda, CloudTrail, GuardDuty, AWS Config, Security Hub, EventBridge, VPC Flow Logs
**Attack Tools:** Pacu, AWS CLI, ScoutSuite (audit), Prowler (audit)
**Vulnerable Targets:** CloudGoat (Rhino Security Labs)
**Infrastructure-as-Code:** Terraform (for repeatable teardown)

---

## Cost & Safety

This lab is built around AWS free tier with strict tear-down discipline:
- Dedicated AWS account (isolated from any personal AWS use)
- Root MFA enabled, root never used for daily work
- Billing alarm set at **$5** to catch runaway costs early
- All paid resources documented with hourly cost
- Each phase includes a destroy step

**Estimated total cost if disciplined: $0–$15 over the full project.**

---

## Connection to Google Cybersecurity Certificate

This lab is the practical capstone that extends the coursework I completed in the [Google Cybersecurity Professional Certificate](../../README.md):
- **Module 3 (Networks):** VPC architecture, VPC Flow Logs, network-level detections
- **Module 5 (Assets/Threats):** Asset inventory and risk assessment applied to cloud resources
- **Module 6 (Detection & Response):** Live SIEM-style detection engineering in CloudTrail/GuardDuty
- **Module 7 (Python):** Custom detection scripts (coming with Module 7)

---

*Project status: Phase 1 — Foundation & Safety Setup (started 2026-05-13)*
