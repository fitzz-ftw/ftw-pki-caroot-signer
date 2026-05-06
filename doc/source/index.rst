.. ftw-devtools documentation master file

ftw-devtools: The Swiss Army Knife for Testing & Git Workflows
==============================================================

`ftw-devtools` is a comprehensive suite of utilities designed to bring 
order to complex development environments. Whether you are battling 
side effects in your test suite or wrestling with messy Git histories, 
this toolkit provides the necessary abstractions to keep your project 
clean and maintainable.

Core Pillars:
-------------

* **Isolated Testing Infrastructure**: 
  Stop letting your tests pollute your `$HOME` directory. With 
  `TestHomeEnvironment`, you get a pristine, sandboxed environment 
  for every test run, ensuring reproducibility and safety.

* **Git & Workflow Automation**: 
  Take the friction out of repository management. From high-level API 
  access to specialized CLI tools like `ftwchangelog`, we automate the 
  tedious parts of your version control workflow.

* **Documentation-Driven Testing**: 
  Bridge the gap between your code and your manuals. Our helpers 
  ensure that your documentation stays in sync with your actual 
  command-line output.

.. toctree::
   :maxdepth: 1
   :caption: Quick Start Guide:

   devel/get_started_run_programms.ci


.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   index_get_started

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation:

   devel/ftw_modules

.. toctree::
   :maxdepth: 1
   :caption: Project Information:

   about
   changelog_link
   license_lgpl21
   genindex
   modindex



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

