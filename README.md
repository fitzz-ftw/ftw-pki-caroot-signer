# ftw-pki-caroot-signer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]

A specialized signing utility within the **ftw-pki** suite, dedicated to the Root CA signing process.

## 🛠 Features

* **Intermediate Issuance:** Strictly designed to sign Intermediate CAs. It does not support signing leaf certificates (end-entities).
* **Root Authority Integration:** Built to operate with the Root CA structures managed by `ftw-pki-caroot`.
* **Standard Enforcement:** Ensures that all issued intermediate certificates comply with the required X.509 extensions and security profiles.

## 📖 Documentation & Usage

The `ftwpkicarootsigner` is the primary tool for establishing the second tier of the PKI hierarchy.

* **Usage:** Processes CSRs provided by the intermediate component. Run `ftwpkicarootsigner --help` for available commands and options.
* **Operational Security:** This tool requires access to the Root CA private key and should be operated according to your organization's security policy.
* **Technical Details:** Further information on the signing logic is available in the `doc/source/` directory.

## 📄 License

This project is licensed under the **LGPL v2.1 (or later)**.

---
© 2026 ftw-pki Contributors
