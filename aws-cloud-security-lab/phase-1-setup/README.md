# Phase 1 — Foundation & Safety Setup

**Objective:** Get a hardened, free-tier-safe AWS lab environment ready before any attack work begins.

This phase is unglamorous but **absolutely critical**. Skipping it is how people end up with $400 surprise AWS bills, leaked credentials on GitHub, or a compromised personal AWS account. SOC analysts who can speak to AWS account hygiene stand out — this phase teaches you that.

---

## Why these steps matter (the SOC analyst framing)

Every step below corresponds to a real-world security control that SOC analysts check during cloud audits:

| Step | Real-world equivalent |
|------|----------------------|
| Dedicated lab account | **Account segmentation** — production isolation |
| MFA on root | **CIS AWS Benchmark 1.5** — root MFA control |
| Billing alarm | **Cost anomaly detection** — common SOC alert source |
| IAM user (not root) | **CIS AWS Benchmark 1.7** — never use root |
| AWS CLI w/ profile | **Programmatic access hygiene** |
| CloudTrail enabled | **CIS AWS Benchmark 3.1** — foundational logging |

When you describe this lab in an interview, you can say *"I implemented CIS AWS Benchmark Section 1 and Section 3 controls."* That's hiring-manager language.

---

## Checklist

- [ ] **1.1** — Create a **dedicated AWS account** for this lab (separate from any personal AWS use)
- [ ] **1.2** — Enable **MFA on the root user** (use phone authenticator app)
- [ ] **1.3** — Set a **billing alarm at $5** so you get an email before anything goes wrong
- [ ] **1.4** — Create an **IAM user** named `lab-admin` with AdministratorAccess + console + access keys
- [ ] **1.5** — Install **AWS CLI v2** on your machine
- [ ] **1.6** — Configure the CLI with a named profile (`aws configure --profile lab-admin`)
- [ ] **1.7** — Enable **CloudTrail** with a multi-region trail (free tier covers this)
- [ ] **1.8** — Verify everything by running `aws sts get-caller-identity --profile lab-admin`

---

## Evidence to capture for the portfolio

For each step, save a screenshot in `../screenshots/phase-1/` with naming `1.X-description.png`:
- `1.1-account-created.png` — the new account dashboard
- `1.2-mfa-enabled.png` — IAM dashboard showing MFA active on root
- `1.3-billing-alarm.png` — CloudWatch alarm in OK state
- `1.4-iam-user.png` — IAM users list showing `lab-admin`
- `1.7-cloudtrail-active.png` — CloudTrail trail showing "Logging: ON"
- `1.8-cli-verified.png` — terminal output of `get-caller-identity`

These screenshots become the evidence in your Phase 1 writeup.
