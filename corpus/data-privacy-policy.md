# Data Privacy Policy

**Effective Date:** January 1, 2025
**Policy Owner:** Legal Department & Information Security
**Applies To:** All employees, contractors, and third parties handling Meridian Technologies data

---

## 1. Purpose

This policy establishes the principles and requirements for the collection, processing, storage, and disposal of personal and sensitive data at Meridian Technologies. We are committed to protecting the privacy of our employees, customers, partners, and all individuals whose data we handle.

## 2. Scope

This policy applies to all personal data processed by Meridian Technologies, whether in electronic or physical form, including:
- Employee personal information
- Customer data
- Vendor and partner data
- Job applicant data
- Website visitor data

## 3. Data Privacy Principles

All data processing activities must adhere to the following principles:

1. **Lawfulness and Transparency**: Data is collected and processed lawfully with clear disclosure to data subjects
2. **Purpose Limitation**: Data is collected for specific, explicit, and legitimate purposes only
3. **Data Minimization**: Only data necessary for the stated purpose is collected
4. **Accuracy**: Data is kept accurate and up to date
5. **Storage Limitation**: Data is retained only as long as necessary for its purpose
6. **Integrity and Confidentiality**: Data is protected against unauthorized access, loss, or destruction
7. **Accountability**: We can demonstrate compliance with these principles

## 4. Data Collection

### 4.1 Employee Data

The company collects the following categories of employee data:
- **Identity data**: Full name, date of birth, government-issued ID numbers
- **Contact data**: Home address, personal email, phone number, emergency contacts
- **Employment data**: Job title, department, compensation, performance reviews
- **Financial data**: Bank account details for payroll, tax information
- **Health data**: Benefits enrollment, accommodation requests (limited access)
- **IT usage data**: Login records, device information, email metadata

### 4.2 Customer Data

Customer data collection is limited to:
- Business contact information
- Contract and billing details
- Service usage data
- Support ticket history
- Communication preferences

### 4.3 Consent

Where consent is required as the legal basis for processing, it must be:
- Freely given
- Specific to the purpose
- Informed (clear explanation of what data is collected and why)
- Documented and auditable
- Revocable at any time

## 5. Data Storage and Security

### 5.1 Storage Locations

Personal data may only be stored in:
- Company-approved cloud services (currently: Google Workspace, AWS, Salesforce)
- Company-managed databases with encryption at rest
- Encrypted company-issued devices
- Locked physical cabinets (for paper records) in secured offices

Personal data must **never** be stored on:
- Personal devices or storage media
- Unapproved cloud services (e.g., personal Dropbox, Google Drive)
- Unencrypted USB drives
- Shared network drives without access controls

### 5.2 Encryption Requirements

| Data Type | At Rest | In Transit |
|-----------|---------|------------|
| Public | Optional | Recommended (TLS) |
| Internal | Recommended | Required (TLS 1.2+) |
| Confidential | Required (AES-256) | Required (TLS 1.2+) |
| Restricted (PII, financial) | Required (AES-256) | Required (TLS 1.3) |

### 5.3 Access Controls

- Access to personal data follows the principle of **least privilege**
- All access must be role-based and approved by data owners
- Access reviews are conducted **quarterly** by department managers
- Privileged access requires MFA and is logged

## 6. Data Retention

### 6.1 Retention Periods

| Data Category | Retention Period | After Period |
|--------------|-----------------|--------------|
| Employee records | 7 years after termination | Secure deletion |
| Customer contracts | 10 years after expiration | Secure deletion |
| Financial records | 7 years | Archive then delete |
| Email communications | 3 years | Auto-deletion |
| Application/resume data | 2 years | Secure deletion |
| Website analytics | 26 months | Anonymization |
| CCTV footage | 90 days | Auto-deletion |

### 6.2 Secure Deletion

When data reaches the end of its retention period:
- Electronic data must be securely wiped using approved tools (minimum DoD 5220.22-M standard)
- Physical documents must be cross-cut shredded
- Backup copies must be deleted within 30 days of main data deletion
- Deletion must be documented in the Data Retention Log

## 7. Data Subject Rights

Individuals whose data we hold have the following rights:

### 7.1 Right of Access

Individuals may request a copy of all personal data we hold about them. Requests must be fulfilled within **30 days**.

### 7.2 Right to Rectification

Individuals may request correction of inaccurate personal data. Corrections must be made within **15 business days**.

### 7.3 Right to Deletion

Individuals may request deletion of their personal data when:
- The data is no longer necessary for its original purpose
- They withdraw consent
- There is no overriding legitimate interest or legal requirement for retention

### 7.4 Right to Data Portability

Individuals may request their data in a structured, machine-readable format (CSV or JSON).

### 7.5 Submitting Requests

Data subject requests should be submitted to:
- Email: privacy@meridiantech.com
- Mail: Privacy Office, Meridian Technologies, 100 Innovation Drive, Suite 500, San Francisco, CA 94105
- Employee self-service: HR Portal → Privacy → Data Request

## 8. Data Breach Response

### 8.1 Breach Definition

A data breach is any unauthorized access, disclosure, alteration, or destruction of personal data, whether intentional or accidental.

### 8.2 Response Procedure

1. **Detect and contain** (within 1 hour): Isolate affected systems, preserve evidence
2. **Assess** (within 4 hours): Determine scope, type of data affected, number of individuals impacted
3. **Notify internally** (within 8 hours): Inform CISO, Legal, and executive leadership
4. **Notify regulators** (within 72 hours): File required notifications with applicable authorities (e.g., state attorneys general, supervisory authorities under GDPR)
5. **Notify affected individuals** (within 5 business days): Clear communication about what happened, what data was affected, and recommended protective actions
6. **Remediate** (ongoing): Implement fixes, update policies, conduct post-incident review

### 8.3 Breach Notification

Breach notifications to affected individuals must include:
- Nature of the breach
- Categories and approximate number of records affected
- Likely consequences
- Measures taken or proposed to address the breach
- Contact information for further questions

## 9. Third-Party Data Processing

### 9.1 Vendor Requirements

Third parties processing personal data on behalf of Meridian Technologies must:
- Sign a Data Processing Agreement (DPA)
- Demonstrate adequate security measures (SOC 2 Type II or equivalent)
- Agree to data breach notification within 24 hours
- Allow audit rights
- Delete or return all data upon contract termination

### 9.2 International Data Transfers

Transfers of personal data outside the employee's or customer's country of residence require:
- Standard Contractual Clauses (SCCs) or equivalent legal mechanism
- Data transfer impact assessment
- Legal department approval

## 10. Training

All employees must complete data privacy training within 30 days of hire and annually thereafter. Employees handling restricted data must complete additional specialized training.

## 11. Contact

For privacy-related questions, contact the Privacy Office at privacy@meridiantech.com or extension 5100.
