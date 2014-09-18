enumerator
==========

Contributors:

-  Erik Dominguez (IRC: Maleus \| Twitter: @Maleus21) (original concept
   and script author, Maleus@overflowsecurity.com) - http://overflowsecurity.com
-  Steve Coward (IRC: felux \| Twitter: @sugarstackio) -
   http://sugarstack.io

enumerator is a tool built to assist in automating the often tedious
task of enumerating a target or list of targets during a penetration
test.

enumerator is built around the Kali Linux distro. To use this on other
Linux distros, please ensure the following tools are installed:

-  nmap
-  nikto, dirb (http enumeration)
-  hydra (ftp enumeration)
-  enum4linux (netbios enumeration)

**Windows is NOT supported at this time.**

Available Service Modules
-------------------------

-  FTP (hydra ftp login enumeration, nmap ftp NSE scripts)
-  HTTP (nikto scan, dirb directory enumeration)
-  Netbios (enum4linux scan)
-  RPC (showmount output)
-  SSH (hydra ssh login enumeration, nmap ssh NSE ssh-hostkey
   enumeration)

Changelog
---------

**v0.1.4** - Added SSH service module, changed all bruteforce options to
use 'tiny' credentials file instead of 'micro', reverted nmap TCP scan
options, minor bug fixes.

**v0.1.3** - enumerator now takes either a file path or single host
parameter to use.

**v0.1.2** - Refactored service classification rules out to individual
service modules and updated class GenericService to validate new service
rules. Created ProcessManager to handle process related tasks.

**v0.1.1** - Corrected issue with flooding system with processes, now
moved to use multiprocessing.Pool().

Installation
------------

While not required, it is advised to create a virtualenv for enumerator
to avoid conflicts with different versions of required packages. If
you're unfamiliar with virtualenv, please follow `this
guide <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__.

Use `pip <http://pip.readthedocs.org/en/latest/installing.html>`__ to
install the required libraries:

.. code:: sh

    (venv) $ pip install enumerator

or alternatively, if you have cloned the enumerator repository:

.. code:: sh

    (venv) $ python setup.py install

Usage
-----

To run, enumerator takes one of two parameters; either a file path to a
text file with a list of IP addresses, one per line.

-  ``-f``, ``--file`` - path to a text file with a list of IP addresses,
   one per line.
-  ``-s``, ``--single`` - a single IP address.

.. code:: sh

    (venv) $ enumerator -f /root/Desktop/hosts.txt

.. code:: sh

    (venv) $ enumerator -s 10.1.1.215

enumerator will then asynchronously begin scanning using nmap. Once nmap
finishes, the nmap results are parsed and passed to a system which,
based upon a simple set of rules, delegates further service-level
enumeration to service-specific modules found in ``lib/``. Each service
module defines specific enumeration applications to be run, and will run
each process against the target, writing any results to file for review.

Currently, enumerator output is very minimal, so it's safe to say that
when the enumerator script finishes, all hosts have been thoroughly
scanned. Future versions of enumerator will have better in-time
reporting of enumeration progress. Results are saved in ``results/``,
and each host will have their own folder, within which all enumeration
process output is saved for review once enumerator completes.

Extending enumerator
--------------------

enumerator is designed to be (relatively) easily extended for additional
service enumeration! Follow these steps to add your own additional
service enumeration:

Creating a NEW service module:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Create folder in ``lib/`` for your service module and related files.
-  Create service module file and \_\_init\_\_.py inside the folder
   created above.
-  The service module should be identical in syntax to existing service
   modules.
-  ``SERVICE_DEFINITION`` is a special set of key:value rules to
   classify a service. Details below.
-  ``PROCESSES`` should contain the literal command(s) to be run. Follow
   the named parameter syntax for any variable strings.
-  Update the ``params`` dictionary within the ``scan()`` method to
   match parameterized string vars set in ``PROCESSES``.
-  In ``lib/delegator.py``, import your new module along with the
   existing module imports.
-  In ``lib/delegator.py``, instantiate your service module and add the
   object to the ``service_modules`` list.

In order to test a newly created service module, it is much easier to
test by invoking the module directly as opposed to running enumerator.
Make sure that your new service module follows the same syntax as
existing module scripts at the very bottom of the script. Update those
calls to match the syntax required for your new service module. To run,
use the following syntax from the root directory of enumerator,
replacing names and input parameters as needed:

.. code:: sh

    (venv) $ python -m enumerator.lib.<service>.<service> <ip> <port> <output directory>

Updating an existing service module:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  To add a new service enumeration command to an existing module,
   simply update ``PROCESSES`` with the command to be invoked. Be sure
   that any named parameters are passed in the ``scan()`` call.

Creating and Updating service definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``SERVICE_DEFINITION`` defines what attributes classify a particular
service. Two keys, ``service`` and ``port`` are available to define the
service. Following two examples and how they translate:

-  ``service:ftp`` - The value ``'ftp'`` should be present in nmap's
   'service' value.
-  ``service:http,-proxy or port:8081`` - The value ``'http'`` should be
   in 'service', the value ``'proxy'`` should **not** be in 'service' or
   the value ``'port'`` should contain the value ``'8081'``.

Updating nmap process command line parameters:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally speaking, editing these defined parameters may negatively
impact the service enumeration modules, so take care with what is being
modified! Configurable ``nmap`` options such as type of TCP connection
syntax, port ranges may certainly be modified to suit the specific use
case. These changes are made in ``lib/nmap.py`` in the ``PROCESSES``
constant defined near the top of the script.

Additional Information
======================

enumerator is being actively maintained! The ``TODO`` file will be kept
updated with various known bug fixes, minor or major features to be
worked on. If you're interested in working on a new feature or would
like to submit new service enumeration modules to the project, by all
means fork us! Maleus and felux (Steve Coward) are always around on IRC
if you'd like to join us! You can find us on **Freenode** at
**#overflowsec**.
