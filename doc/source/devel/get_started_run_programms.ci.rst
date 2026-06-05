The Signing Programm
######################

.. SECTION - Setup

>>> test_data_pre= "test_ok_data2"
>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")
>>> env.setup(True)
>>> env.clean_home()
>>> env.clean_output()

.. !SECTION
.. SECTION - Prepare

>>> ca_pki_path = env.copy2cwd(f"{test_data_pre}/ca_root.pki",
...             "ca_root.pki")

>>> cert_path = env.copy2cwd(f"{test_data_pre}/Muster-Verband-Hamburg-Regional-CA_Hamburg.csr",
...             "M-V-HH-CA_Hamburg.csr")

>>> cert_name = cert_path.name


>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "secret"

>>> def stub_keyboard_interrupt(prompt:str):
...     raise KeyboardInterrupt

>>> def stub_exception(prompt:str):
...     raise Exception("Test exception!")

>>> import getpass
>>> getpass.getpass = getpasswd


>>> cmd_line = " --policy-name intermediate"
>>> cmd_line += " -c ca_root.pki "
>>> cmd_line += " carootsecret "
>>> cmd_line += f" {cert_name} "

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--policy-name', 'intermediate', 
 '-c', 'ca_root.pki', 
 'carootsecret', 
 'M-V-HH-CA_Hamburg.csr']

.. !SECTION

>>> from ftwpki.baselibs.utils import print_error

>>> import ftwpki.ca_root_signer.programms

>>> ftwpki.ca_root_signer.programms.report_error = print_error

>>> from ftwpki.ca_root_signer.programms import prog_ca_root_signing

>>> db_path = Path("db/index.txt")

>>> db_path.is_file()
False

>>> prog_ca_root_signing(sys_argv)
Enter Password:
0

>>> db_path.is_file()
True

>>> db_path.read_text() #doctest: +ELLIPSIS
'V\t...\t\t...\t...\tCN=Muster-Verband Hamburg Regional CA...'

>>> prog_ca_root_signing(sys_argv)
Enter Password:
0

>>> print(db_path.read_text()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
V   ...           ...        ... CN=Muster-Verband Hamburg Regional CA...
V   ...           ...        ... CN=Muster-Verband Hamburg Regional CA...
<BLANKLINE>

>>> cmd_line = " --policy-name intermediate "
>>> cmd_line += " carootsecret "
>>> cmd_line += f" {cert_name} "

>>> sys_argv= shlex.split(cmd_line) 

>>> prog_ca_root_signing(sys_argv) 
the following arguments are required: -c/--cert/--certificate
1

>>> cmd_line = " --policy-name intermediate "
>>> cmd_line += " -c ca_root.pki "
>>> cmd_line += " -CN no "
>>> cmd_line += " -OU no "
>>> cmd_line += " carootsecret "
>>> cmd_line += f" {cert_name} "

>>> sys_argv= shlex.split(cmd_line) 

>>> prog_ca_root_signing(sys_argv) 
While policyvalidation following missmatch occurs:
    - [commonName]: DISALLOWED
    - [organizationalUnitName]: DISALLOWED
1


>>> cmd_line = " --policy-name intermediate"
>>> cmd_line += " -c ca_root.pki "
>>> cmd_line += " carootsecret "
>>> cmd_line += f" {cert_name} "

>>> sys_argv= shlex.split(cmd_line) 
>>> getpass.getpass=stub_keyboard_interrupt
>>> prog_ca_root_signing(sys_argv)
2

>>> getpass.getpass=stub_exception
>>> prog_ca_root_signing(sys_argv)
Test exception!
1


.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION
