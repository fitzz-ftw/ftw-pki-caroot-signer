Running the programm Successfully and Errors
==============================================

.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path

>>> _ = env.copy2cwd("ca_root_conf.toml")
>>> Path("privat").mkdir(parents=True, exist_ok=True)
>>> _ = env.copy2cwd("privat/testpasswd")
>>> _ = env.copy2cwd("privat/ca.key.pem")
>>> _ = env.copy2cwd("ca_public/ca.cert", "ca.cert")
>>> _ = env.copy2cwd("Fitzz-TeXnik-WeltSomewherecity.csr")

>>> def stub_input(prompt:str):
...     print(prompt)
...     return "strenggeheim"

>>> import getpass
>>> getpass.getpass = stub_input

>>> cmd_line =  "--conf-file ca_root_conf.toml"
>>> cmd_line += " -k privat/ca "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " --policy-name intermediate"
>>> cmd_line += " -c ca.cert"
>>> cmd_line += " testpasswd"
>>> cmd_line += " Fitzz-TeXnik-WeltSomewherecity.csr"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 'ca_root_conf.toml', 
 '-k', 'privat/ca', 
 '--private-dir', 'privat', 
 '--policy-name', 'intermediate',
 '-c', 'ca.cert',
 'testpasswd',
 'Fitzz-TeXnik-WeltSomewherecity.csr']


.. !SECTION
.. SECTION - Start programm function

>>> from ftwpki.ca_root_signer.programms import prog_ca_root_singing

>>> prog_ca_root_singing(sys_argv)
Enter Password:
0

..SECTION dn missmatch





..!SECTION dn missmatch

>>> cmd_line =  "--conf-file ca_root_conf.toml"
>>> cmd_line += " -k privat/ca.key.pem "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " --policy-name intermediate"
>>> cmd_line += " -c ca.cert"
>>> cmd_line += " -ST no"
>>> cmd_line += " testpasswd"
>>> cmd_line += " Fitzz-TeXnik-WeltSomewherecity.csr"
>>> sys_argv= shlex.split(cmd_line) 
>>> prog_ca_root_singing(sys_argv) #doctest: +NORMALIZE_WHITESPACE
  - [stateOrProvinceName]: DISALLOWED
1

>>> cmd_line =  "--conf-file ca_root_conf.toml"
>>> cmd_line += " -k privat/ca.key.pem "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " --policy-name intermediate"
>>> cmd_line += " -c ca.cert"
>>> cmd_line += " -ST MACH"
>>> cmd_line += " testpasswd"
>>> cmd_line += " Fitzz-TeXnik-WeltSomewherecity.csr"
>>> sys_argv= shlex.split(cmd_line) 
>>> prog_ca_root_singing(sys_argv) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
argument -ST/--stateOrProvinceName: invalid choice: 'MACH' (choose from ...)
2

.. SECTION - Template

>>> cmd_line =  "--conf-file ca_root_conf.toml"
>>> cmd_line += " -k privat/ca "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " --policy-name intermediate"
>>> cmd_line += " -c ca.cert"
>>> cmd_line += " testpasswd"
>>> cmd_line += " Fitzz-TeXnik-WeltSomewherecity.csr"
>>> sys_argv= shlex.split(cmd_line) 
>>> prog_ca_root_singing(sys_argv)
Enter Password:
0


.. !SECTION - Template

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
