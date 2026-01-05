# 🛡️ Secure Inventory Management System (UniKL IKB 21503)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/OWASP-ASVS%20Compliant-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Build-Secure-brightgreen?style=for-the-badge)

## 📝 Project Description
This is a high-security *Inventory Management System* developed as part of the *IKB 21503: Secure Software Development* course at UniKL. The application is designed to handle sensitive warehouse data while implementing rigorous defense-in-depth strategies. 

By integrating *DevSecOps* basics, we ensure that the application is resilient against the *OWASP Top 10* vulnerabilities, specifically focusing on Injection, Broken Access Control, and Identification Failures.

---

## 🚀 Security Architecture & Features

### 🔐 1. Identity & Access Management (ASVS V2)
* *Multi-Factor Authentication (MFA)*: Every login requires a 6-digit verification token sent via TLS-encrypted email.
* *Cryptographic Entropy*: Tokens are generated using the secrets library for non-predictable, high-entropy random numbers.
* *Anti-Automation (CAPTCHA): Integrated **Simple CAPTCHA* on both Registration and Login forms to neutralize bot-driven credential stuffing.

### 🛡️ 2. Defense Mechanisms (ASVS V4/V7)
* *Brute-Force Protection*: 3-strike policy—after three failed login attempts, the account is locked for 15 minutes via a database-backed cache.
* *Information Exposure Control*: Set DEBUG = False to hide technical metadata, stack traces, and local file paths.
* *Custom Error Intercepts: Branded **403 Access Denied* and *404 Signal Interrupted* pages to obfuscate internal URL structures.

### 📜 3. Auditing & Integrity (ASVS V8)
* *Immutable Audit Logs*: Tracks critical actions (Add/Delete/Export) and logs "SECURITY ALERTS" for suspicious lockout events.
* *Output Encoding: Automatic HTML escaping to prevent **Cross-Site Scripting (XSS)*.
* *Environment Isolation*: Sensitive keys (SECRET_KEY, SMTP credentials) are stored in .env and excluded from version control.

---

## 🛠️ Installation & Setup

Follow these steps to deploy the secure environment locally:

1.  *Clone the Repository*
    bash
    git clone [https://github.com/uzairblip/secure_project123.git](https://github.com/uzairblip/secure_project123.git)
    cd secure_project123
    

2.  *Initialize Virtual Environment & Dependencies*
    bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    

3.  *Configure Environment Variables*
    * Duplicate .env.example and rename it to .env.
    * Input your SECRET_KEY, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD.

4.  *Database & Security Cache Initialization*
    bash
    python manage.py migrate
    python manage.py createcachetable  # 🛡️ REQUIRED for the lockout system
    python manage.py collectstatic     # 🎨 REQUIRED to load theme with DEBUG=False
    

---

## 🏃 Execution
Start the secure development server:
```bash
python manage.py runserver