The Signing Programm
######################

.. SECTION - Setup

>>> test_data_pre= "data-root-signer"
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")
>>> env.setup(True)
>>> env.clean_output()

.. !SECTION
.. SECTION - Prepare

>>> ca_pki_path = env.copy2cwd(f"{test_data_pre}/ca_root_conf.pki",
...             "ca_root.pki")

>>> cert_path = env.copy2cwd(f"{test_data_pre}/M-V-HH-CA.csr",
...             "M-V-HH-CA.csr")

>>> cert_name = cert_path.name



>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "secret"



>>> cmd_line = " --policy-name intermediate"
>>> cmd_line += " -c ca_root.pki "
>>> cmd_line += " -P 1"
>>> cmd_line += " -CN no " #doctest: +SKIP
>>> cmd_line += " carootsecret "
>>> cmd_line += f" {cert_name} "

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE -SKIP
['--policy-name', 'intermediate', 
 '-c', 'ca_root.pki',
  '-P', '1',
 'carootsecret', 
 'M-V-HH-CA.csr']

.. !SECTION



.. SECTION - Programm Signing

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn_policy, toml2ext, toml2dn
>>> from ftwpki.baselibs.cli_parser import CSRSigningParser
>>> from ftwpki.baselibs.policies import IntermediatePolicy
>>> from ftwpki.baselibs.configuration import RootSignerPKIConfig


>>> pre_parser = CSRSigningParser(add_help=False, allow_abbrev=False)
>>> pre_args , _ = pre_parser.parse_known_args(sys_argv)

>> pre_args


>>> config = RootSignerPKIConfig(pre_args.certificate)

>>> config._paths #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'config_path': ...Path('.../.config/ftwpki'), 
 'data_path': ...Path('.../.local/share/ftwpki'), 
 'passphrases': ...Path('.../.config/ftwpki/.private'), 
 'zip': ...Path('.../.config/ftwpki/.private')}

>>> config.in_zip
['private_keys', 'certs', 'chains', 'policies']




>>> config.handle_pki_file()



>>> config.passphrases.as_posix() # doctest: +ELLIPSIS
'.../ftwpki/.private'

>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#zip#', 
 'zip': '#config#.private', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'passphrases': '#config#.private', 
 'policies': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}

>>> temp_key_pem = "CA.key.pem"


>>> config.private_key(temp_key_pem) #doctest: +ELLIPSIS
b'-----BEGIN ENCRYPTED PRIVATE KEY---...'

>>> config.fullchain #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
[<Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>, 
 <Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>]

>>> config.policy_files
['ca_root.policy']

>>> file_defaults = config.get_dn_policies('ca_root.policy', 'intermediate')
>>> file_defaults #doctest: +NORMALIZE_WHITESPACE
{'countryName': 'match', 
 'organizationName': 'match', 
 'commonName': 'supplied', 
 'localityName': 'supplied', 
 'organizationalUnitName': 'optional', 
 'stateOrProvinceName': 'optional'}


>>> ca_parser = CSRSigningParser(prog="ftwpkicasign")
>>> ca_parser.set_defaults(**file_defaults)


>>> extention = config.get_extentions('ca_root.policy', 'intermediate')
>>> extention #doctest: +NORMALIZE_WHITESPACE
{'ocspURI': 'http://ocsp.example.org/root', 
 'crlURI': 'http://pki.example.org/rsm/regional.crl', 
 'caIssuerURI': 'http://pki.example.org/root/root.crt'}


>>> args = ca_parser.parse_args(sys_argv)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
Namespace(countryName='match', 
     stateOrProvinceName='optional', 
     localityName='supplied', 
     organizationName='match', 
     organizationalUnitName='optional', 
     commonName='supplied', 
     policy_name='intermediate', 
     conf_file=None, 
     key_name=None, 
     private_dir=None, 
     certificate='ca_root.pki', 
     validity_days=365, 
     path_length=1, 
     passphrasefile='carootsecret', 
     certificat_sign_request='M-V-HH-CA.csr', 
     policy={'countryName': 'match', 
          'stateOrProvinceName': 'optional', 
          'localityName': 'supplied', 
          'organizationName': 'match', 
          'organizationalUnitName': 'optional', 
          'commonName': 'supplied'}, 
     private_key='')

.. !SECTION

.. SECTION - Validating

>>> from ftwpki.baselibs.core import (
...     load_certificate_from_pem, 
...     load_csr_from_pem,
...     get_subject_dict,
...     )

>> ca_cert = load_certificate_from_pem(
...      pem_data=Path(args.certificat_sign_request).read_bytes())

>>> config.get_certs() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'ca.crt.pem': <Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>, 
 'user.crt.pem': <Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>, 
 'caroot.crt.pem': <Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA)>, ...)>}

>>> ca_cert = config.own_cert 
>>> ca_cert #doctest: +ELLIPSIS
<Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>

>>> csr = load_csr_from_pem(Path(args.certificat_sign_request).read_bytes())

>>> from ftwpki.baselibs.validate import ValidatorDN

>>> val_dn= ValidatorDN(args.policy,
...          get_subject_dict(ca_cert))
>>> val_dn.validate(get_subject_dict(csr)) 
ValidationResult(is_valid=True, errors=[])

>>> val_dn.validate(get_subject_dict(csr)) #doctest: +NORMALIZE_WHITESPACE +SKIP
Traceback (most recent call last):
     ...
ftwpki.baselibs.exceptions.PKIPolicyValidationError: While policyvalidation 
     following missmatch occurs:
         - [commonName]: DISALLOWED

.. !SECTION - Validating

.. SECTION - Passwordhandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir="")
>>> pwd_man
PasswordManager(private_dir='.')

>>> pass_phrase = pwd_man.decrypt_password_file(
...    config.passphrases / args.passphrasefile, 
...    getpasswd("Enter Password:"))
Enter Password:


.. !SECTION - Passwordhandling

.. SECTION - Signing


>>> from ftwpki.baselibs.core import (
...     load_private_key_from_pem,
...     load_csr_from_pem,
...     save_pem,
...     cert_to_record,
...     )
>>> from ftwpki.baselibs.signer import CertificateSigner

>>> private_key_obj= load_private_key_from_pem(
...             pem_data = config.private_key(temp_key_pem), 
...             passphrase=pass_phrase)

>>> cert_signer = CertificateSigner(
...      ca_cert=ca_cert,
...      ca_key=private_key_obj)

>> print(args.path_length)

>>> policy = IntermediatePolicy(path_length = args.path_length)

>>> from ftwpki.baselibs.validate import validate_and_clamp_validity

>>> validity_days= validate_and_clamp_validity(ca_cert, args.validity_days)

>>> signed_cert = cert_signer.sign(csr=csr, 
...     policy=policy, 
...     validity_days=validity_days.actual_days,
...     **extention)


>>> signed_pem = cert_signer.get_pem(signed_cert)
>>> target_path = Path(args.certificat_sign_request).with_suffix(".crt.pem")

>>> save_pem(data = signed_pem, 
...     target_path=target_path, 
...     is_private = True)

.. !SECTION - Signing

.. SECTION - Transferfile
>>> from ftwpki.baselibs.package import PKIPackage

>>> out_package = PKIPackage()
>>> out_package.recipient_cert = signed_cert
>>> out_package.private_key = private_key_obj
>>> out_package.caroot_cert = config.own_cert

>>> out_package.ca_cert = config.own_cert

>>> out_package.fullchain.extend(config.fullchain)

>>> out_package.fullchain #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
[<Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>, 
 <Certificate(subject=<Name(...CN=Muster-Verband Bundesverband Root CA...)>, ...)>]

>>> out_package.to_encrypt=True

False

>>> out_package.save(args.certificat_sign_request).as_posix()
'M-V-HH-CA.spki'

.. !SECTION - Transferfile

.. SECTION - Testing only

>>> with transfer_file_path.open("rb") as f: #doctest: +SKIP
...     f.readline()
...     f.readline()
...     f.readline()
...     f.readline()
b'MIME-Version: 1.0\n'
b'Content-Disposition: attachment; filename="smime.p7m"\n'
b'Content-Type: application/pkcs7-mime; smime-type="enveloped-data"; name="smime.p7m"\n'
b'Content-Transfer-Encoding: base64\n'

.. !SECTION

.. SECTION - Database openssl compatible

>>> from ftwpki.baselibs.openssl_comp import DbOpensslFile
>>> db_dir = Path("db")


.. !SECTION - Database openssl compatible

.. !SECTION - Programm Signing

.. SECTION - Check Result 

>>> from ftwpki.baselibs.utils import get_cert_text

>>> print(get_cert_text(target_path.as_posix())) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
Subject:
     CN=Muster-Verband Hamburg Regional CA,...
Issuer:
     CN=Muster-Verband Bundesverband Root CA,...
Serial Number:
     ...
Not Before:
     20...
Not After:
     20...
Version:
     v3
Extensions:
     basicConstraints:
          CA=Yes, path_length=1
     keyUsage:
          key_cert_sign, crl_sign
     authorityKeyIdentifier:
          b...
     authorityInfoAccess:
          OCSP: http://ocsp.example.org/root
          caIssuers: http://pki.example.org/root/root.crt
     cRLDistributionPoints:
          http://pki.example.org/rsm/regional.crl
     subjectKeyIdentifier:
          b...

.. !SECTION - Check Result 


.. SECTION - Teardown

>> env.clean_output()

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
