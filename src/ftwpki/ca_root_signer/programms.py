# File: src/ftwpki/client_server/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""
#DOC - Module docstring

import getpass
from pathlib import Path

from ftwpki.baselibs.cli_parser import (
    CSRSigningParser,
    TomlPreParser,
)
from ftwpki.baselibs.configuration import PKIPackage, RootSignerPKIConfig_DEV
from ftwpki.baselibs.core import (
    cert_to_record,
    get_subject_dict,
    load_certificate_from_pem,
    load_csr_from_pem,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.exceptions import PKIPolicyValidationError
from ftwpki.baselibs.openssl_comp import DbOpensslFile
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.policies import IntermediatePolicy
from ftwpki.baselibs.signer import CertificateSigner
from ftwpki.baselibs.toml_utils import toml2dn_policy, toml2ext
from ftwpki.baselibs.transport import encrypt_transport_package
from ftwpki.baselibs.utils import report_error
from ftwpki.baselibs.validate import ValidatorDN, validate_and_clamp_validity


# SECTION - Programm Signing
def prog_ca_root_signing(argv: list[str] | None = None) -> int:
    """
    Entry point for signing Certificate Signing Requests (CSRs). (rw)

    Validates the CSR against the CA policy, signs it using the Root-CA key,
    and prepares the transport package.

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for validation error, 2 for other errors).
    """
    try:
        # SECTION - Configuration
        pre_parser = TomlPreParser()
        pre_args, _ = pre_parser.parse_known_args(argv)
        ca_parser = CSRSigningParser()
        # for k, v in toml2_dn_policy(argv).items():
        #     print(f"{k}: {v}")
        file_conf = toml2dn_policy(pre_args.conf_file, pre_args.policy_name) 
        ca_parser.set_defaults(**file_conf)
        # ca_parser.set_defaults(**toml2_dn_policy(argv))
        extention = toml2ext(pre_args.conf_file, pre_args.policy_name)
        args = ca_parser.parse_args(argv)
        # !SECTION - Configuration

        # print(f"{args.policy}")
        # SECTION - Validating
        ca_cert = load_certificate_from_pem(pem_data=Path(args.certificate).read_bytes())
        csr = load_csr_from_pem(Path(args.certificat_sign_request).read_bytes())
        val_dn = ValidatorDN(args.policy, get_subject_dict(ca_cert))
        validate_result = val_dn.validate(get_subject_dict(csr),raise_on_error=False)
        if not validate_result.is_valid:
            for error in validate_result.errors:
                print(error)
            return 1
        # !SECTION - Validating

        # SECTION - Passwordhandling
        pwd_man = PasswordManager(private_dir=args.private_dir)
        pass_phrase = pwd_man.decrypt_password_file(
            args.passphrasefile, password=getpass.getpass("Enter Password:")
        )
        # !SECTION - Passwordhandling

        # SECTION - Signing
        private_key_obj = load_private_key_from_pem(
            pem_data=Path(args.private_key).read_bytes(), passphrase=pass_phrase
        )
        cert_signer = CertificateSigner(ca_cert=ca_cert, ca_key=private_key_obj)
        policy = IntermediatePolicy(path_length=args.path_length)
        validity_days = validate_and_clamp_validity(ca_cert, args.validity_days)
        signed_cert = cert_signer.sign(
            csr=csr, policy=policy, validity_days=validity_days.actual_days, **extention
        )
        signed_pem = cert_signer.get_pem(signed_cert)
        target_path:Path = Path(args.certificat_sign_request).with_suffix(".crt.pem")
        save_pem(
            data=signed_pem,
            target_path= target_path,
            is_private=True,
        )
        # !SECTION - Signing

        # SECTION - Transferfile
        zipped_data = encrypt_transport_package(
            signed_cert,  # user_cert
            ca_cert,  # root_ca_cert
            private_key_obj,
            signed_cert,  # recipient_cert
            signed_cert,
            ca_cert,
            name_user=target_path.name,
            name_chain="all.chain.pem",
            name_ca = "ca.crt.pem",
        )

        transfer_file_path = Path(args.certificat_sign_request).with_suffix(".zip.enc")
        transfer_file_path.write_bytes(zipped_data)
        # !SECTION - Transferfile

        # SECTION - Database openssl compatible
        db_dir = Path("db")
        if not db_dir.is_dir():
            db_dir.mkdir(parents=True)
        db_file = DbOpensslFile(db_dir / "index.txt")
        db_file.add_record(
            record=cert_to_record(cert=load_certificate_from_pem(signed_pem), status="V")
        )
        # !SECTION - Database openssl compatible
        return 0
    except Exception as e:
        print(e)
        return 2
# !SECTION - Programm Signing

#SECTION - prog_ca_root_signing_DEV
# DOC - new
def prog_ca_root_signing_DEV(argv: list[str] | None = None) -> int:
    try:
        # SECTION - Configuration
        pre_parser = CSRSigningParser(add_help=False, allow_abbrev=False)
        pre_args , _ = pre_parser.parse_known_args(argv)
        config = RootSignerPKIConfig_DEV(pre_args.certificate)
        config.handle_pki_file()
        file_defaults = config.get_dn_policies('ca_root.policy', 'intermediate')
        ca_parser = CSRSigningParser(prog="ftwpkicasign")
        ca_parser.set_defaults(**file_defaults)
        extention = config.get_extentions('ca_root.policy', 'intermediate')
        args = ca_parser.parse_args(argv)
        # !SECTION - Configuration

        # SECTION - Validating
        ca_cert = config.own_cert
        csr = load_csr_from_pem(Path(args.certificat_sign_request).read_bytes())
        val_dn= ValidatorDN(args.policy,
            get_subject_dict(ca_cert))
        val_dn.validate(get_subject_dict(csr))
        #!SECTION - Validating

        # SECTION - Passwordhandling
        pwd_man = PasswordManager(private_dir="")
        pass_phrase = pwd_man.decrypt_password_file(
            config.passphrases / args.passphrasefile, 
            getpass.getpass("Enter Password:"))
        # !SECTION - Passwordhandling

        # SECTION - Signing
        private_key_obj= load_private_key_from_pem(
            pem_data = config.private_key, 
            passphrase=pass_phrase)
        policy = IntermediatePolicy(pathlength = args.path_length)
        validity_days = validate_and_clamp_validity(ca_cert, args.validity_days)
        cert_signer = CertificateSigner(
            ca_cert=ca_cert,
            ca_key=private_key_obj)
        signed_cert = cert_signer.sign(csr=csr, 
            policy=policy, 
            validity_days=validity_days.actual_days,
            **extention)
        signed_pem = cert_signer.get_pem(signed_cert)
        # !SECTION - Signing

        # SECTION - Transferfile
        out_package = PKIPackage()
        out_package.recipient_cert = signed_cert
        out_package.private_key = private_key_obj
        out_package.caroot_cert = config.own_cert
        out_package.ca_cert = config.own_cert
        out_package.fullchain.extend(config.fullchain)
        out_package.to_encrypt = True
        out_package.save(args.certificat_sign_request)
        # !SECTION - Transferfile

        # SECTION - Database openssl compatible
        db_dir = Path("db")
        if not db_dir.is_dir():
            db_dir.mkdir(parents= True)
        db_file= DbOpensslFile(db_dir/"index.txt")
        db_file.add_record(record=cert_to_record(
            cert = load_certificate_from_pem(signed_pem),
            status = "V")
            )
        #!SECTION - Database openssl compatible
        return 0
    except PKIPolicyValidationError as e:
        report_error(e)
        return 1
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        report_error(e)
        return 1
#!SECTION - prog_ca_root_signing_DEV



if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        # "get_started_programms.ci.rst",
        "get_started_programms_DEV.ci.rst",
        # "get_started_run_programms_DEV.ci.rst",
        # "get_started_run_programms.ci.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
        if test_file.exists():
            print(f"--- Running Doctest for {test_file.name} ---")
            doctestresult = testfile(
                str(test_file),
                module_relative=False,
                verbose=be_verbose,
                optionflags=option_flags,
            )
            test_failed += doctestresult.failed
            test_sum += doctestresult.attempted
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(
                    f"\nKeep going! You already passed {passed_files} files "
                    f"with {test_sum} tests before this hit."
                )
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
