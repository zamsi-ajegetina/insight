# Information Security Policy

**Effective Date:** January 1, 2025
**Policy Owner:** Chief Information Security Officer (CISO)
**Applies To:** All employees, contractors, and third-party users of Meridian Technologies systems

---

## 1. Purpose

This policy establishes the information security standards that all personnel must follow to protect Meridian Technologies' data, systems, and infrastructure from unauthorized access, disclosure, alteration, and destruction.

## 2. Scope

This policy covers all company-owned or managed information systems, networks, applications, data, and devices — including employee-owned devices used for work purposes (BYOD).

## 3. Password Requirements

### 3.1 Password Complexity

All passwords must meet the following minimum requirements:
- At least **14 characters** in length
- Include at least one uppercase letter, one lowercase letter, one number, and one special character
- Must not contain the user's name, username, or common dictionary words
- Must not match any of the user's last 12 passwords

### 3.2 Password Rotation

- Standard users must change passwords every **90 days**
- Privileged/admin accounts must change passwords every **60 days**
- Service account passwords must be rotated every **180 days**

### 3.3 Password Storage

Passwords must never be written down, stored in plain text, shared via email or chat, or saved in browser password managers on shared devices. Use the company-approved password manager (currently 1Password Enterprise) for all credential storage.

## 4. Multi-Factor Authentication (MFA)

### 4.1 MFA Requirements

MFA is mandatory for:
- All VPN connections
- All cloud service logins (email, file storage, project management)
- Administrative access to any system
- Access to financial or HR systems
- Remote access to internal applications

### 4.2 Approved MFA Methods

- Hardware security keys (YubiKey) — **preferred**
- Authenticator apps (Google Authenticator, Microsoft Authenticator)
- Push notifications via company MDM application

SMS-based authentication is **not approved** due to SIM-swapping vulnerabilities.

## 5. Device Security

### 5.1 Company-Issued Devices

All company-issued laptops and mobile devices must:
- Have full-disk encryption enabled (BitLocker for Windows, FileVault for macOS)
- Run the latest approved OS version within 30 days of release
- Have endpoint detection and response (EDR) software installed and active
- Auto-lock after 5 minutes of inactivity
- Be registered in the company MDM (Mobile Device Management) system

### 5.2 BYOD (Bring Your Own Device)

Personal devices used for work purposes must:
- Be registered in the MDM system
- Meet minimum OS version requirements
- Have a PIN or biometric lock enabled
- Allow remote wipe capability for company data only (containerized wipe)
- Not be jailbroken or rooted

### 5.3 Lost or Stolen Devices

Lost or stolen devices must be reported to IT Security within **1 hour** of discovery by emailing security@meridiantech.com or calling the 24/7 security hotline at extension 9111. IT Security will immediately initiate a remote wipe.

## 6. Data Classification

### 6.1 Classification Levels

| Level | Description | Examples |
|-------|------------|----------|
| **Public** | Information intended for public disclosure | Marketing materials, press releases |
| **Internal** | General business information | Meeting notes, internal announcements |
| **Confidential** | Sensitive business information | Financial reports, strategic plans, customer lists |
| **Restricted** | Highly sensitive data with legal/regulatory implications | PII, PHI, payment card data, trade secrets |

### 6.2 Handling Requirements

- **Public**: No special handling required
- **Internal**: Do not share externally without management approval
- **Confidential**: Encrypt in transit and at rest; share only on a need-to-know basis
- **Restricted**: Encrypt at all times; access requires written justification and CISO approval; log all access

## 7. Incident Reporting

### 7.1 What to Report

All suspected security incidents must be reported, including but not limited to:
- Suspected phishing emails or social engineering attempts
- Unauthorized access to systems or data
- Malware or ransomware infections
- Data breaches or data loss
- Physical security breaches (tailgating, unauthorized visitors)
- Unusual system behavior or performance issues

### 7.2 How to Report

Report incidents immediately through any of the following channels:
1. Email: security@meridiantech.com
2. Phone: Extension 9111 (24/7 hotline)
3. Slack: #security-incidents channel
4. In person: Visit the IT Security office (Building A, Room 210)

### 7.3 Response Timeline

- **Critical incidents** (active data breach, ransomware): Response within 15 minutes
- **High-priority incidents** (suspected compromise): Response within 1 hour
- **Medium-priority incidents** (phishing attempt, policy violation): Response within 4 hours
- **Low-priority incidents** (general security questions): Response within 1 business day

## 8. Acceptable Use

### 8.1 Prohibited Activities

The following activities are strictly prohibited on company systems:
- Installing unauthorized software or browser extensions
- Using company resources for personal commercial activities
- Accessing or distributing inappropriate, illegal, or offensive content
- Circumventing security controls (VPN bypass, proxy usage for blocked sites)
- Connecting unauthorized devices to the corporate network
- Sharing login credentials with anyone, including colleagues

### 8.2 Monitoring

Meridian Technologies reserves the right to monitor all activity on company-owned systems and networks. This includes email, web browsing, file access, and application usage. Monitoring is conducted in compliance with applicable laws and is not used for personal surveillance.

## 9. Training

All employees must complete mandatory security awareness training within 30 days of hire and annually thereafter. Training covers phishing awareness, password hygiene, data handling, and incident reporting. Failure to complete training within the required timeframe may result in temporary suspension of system access.

## 10. Enforcement

Violations of this policy may result in disciplinary action up to and including termination of employment and, where applicable, legal action. Severity of consequences will be proportional to the nature and impact of the violation.

## 11. Contact

For security questions or to report an incident, contact the Information Security team at security@meridiantech.com or extension 9111.
