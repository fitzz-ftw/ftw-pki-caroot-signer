# Changelog - ftw-pki-caroot-signer

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3a1] - 2026-05-15

### Added
- First official release as a standalone package `ftw-pki-caroot-signer`.
- Added signing logic for Root CAs to issue certificates.
- Integrated full CLI documentation and README.
- Reached 100% test coverage for the signer logic.

### Changed
- Synchronized version number with the FTW PKI v0.0.3 alpha series.
- Refactored internal imports to use `ftw-pki-base-libs`.

## [0.0.2] - 2026-04-10

### Added
- **Initial Release:** Extracted the signer logic from the experimental tools into this standalone package.
- Added API documentation for protocols and programs.
- Implemented secure transport mechanisms for key handling.
