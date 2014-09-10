enumerator 0.1
=========

&nbsp;
#### Contributors:
* Maleus (original concept and script author) - http://overflowsecurity.com
* Steve Coward (felux) - http://sugarstack.io

enumerator is a tool built to assist in automating the often tedious task of enumerating a target or list of targets during a penetration test.

enumerator is built around the Kali Linux distro. To use this on other Linux distros, please ensure the following tools are installed:

  - nmap
  - nikto, dirb (http enumeration)
  - hydra (ftp enumeration)
  - enum4linux (netbios enumeration)

**Windows is NOT supported at this time.**

Installation
----

While not required, it is advised to create a virtualenv for enumerator to avoid conflicts with different versions of required packages. If you're unfamiliar with virtualenv, please follow [this guide] [1].

Use [pip] [2] to install the required libraries:

```sh
(venv) $ pip install enumerator
```

or alternatively, if you have cloned the enumerator repository:

```sh
(venv) $ python setup.py install
```

Usage
----

To run, enumerator takes a single parameter; a file path to a text file with a list of IP addresses, one per line.

```sh
(venv) $ enumerator /root/Desktop/hosts.txt
```

enumerator will then asynchronously begin scanning each host listed in ``hosts.txt`` using nmap. Once nmap finishes, the nmap results are parsed and passed to a system which, based upon a simple set of rules, delegates further service-level enumeration to service-specific modules found in ``lib/``. Each service module defines specific enumeration applications to be run, and will run each process against the target, writing any results to file for review. 

Currently, enumerator output is very minimal, so it's safe to say that when the enumerator script finishes, all hosts have been thoroughly scanned. Future versions of enumerator will have better in-time
reporting of enumeration progress. Results are saved in ``results/``, and each host will have their own folder, within which all enumeration process output is saved for review once enumerator completes.

Extending enumerator
----

enumerator is designed to be (relatively) easily extended for additional service enumeration! Follow these steps to add your own additional service enumeration:

#### Creating a NEW service module:

* Create folder in ``lib/`` for your service module and related files.
* Create service module file and \_\_init\__\.py inside the folder created above.
* The service module should be identical in syntax to existing service modules.
* The ``PROCESSES`` constant should contain the literal command(s) to be run. Follow the named parameter syntax for any variable strings.
* Update the ``params`` dictionary within the ``scan()`` method to match parameterized string vars set in ``PROCESSES``.
* In ``lib/delegator.py``, import your new module along with the existing module imports.
* Create a new method following the format ``def is_<service_name>`` and use any combination of ``service``, ``port`` and ``state`` to create new service classification rules.
* Add a conditional in ``receive_service_data()`` to instantiate your new service module when the defined service rules are matched.

In order to test a newly created service module, it is much easier to test by invoking the module directly as opposed to running enumerator. Make sure that your new service module follows the same syntax as existing module scripts at the very bottom of the script. Update those calls to match the syntax required for your new service module. To run, use the following syntax from the root directory of enumerator, replacing names and input parameters as needed:

```sh
(venv) $ python -m enumerator.lib.<service>.<service> <ip> <port> <output directory>
```

#### Updating an existing service module:
* To add a new service enumeration command to an existing module, simply update ``PROCESSES`` with the command to be invoked. Be sure that any named parameters are passed in the ``scan()`` call.
* To update service classification rules, edit the rule definition methods in ``lib/delegator.py``.

#### Updating nmap process command line parameters:

Generally speaking, editing these defined parameters may negatively impact the service enumeration modules, so take care with what is being modified! Configurable ``nmap`` options such as type of TCP connection syntax, port ranges may certainly be modified to suit the specific use case. These changes are made in ``lib/nmap.py`` in the ``PROCESSES`` constant defined near the top of the script.

Additional Information
====

enumerator is being actively maintained! The ``TODO`` file will be kept updated with various known bug fixes, minor or major features to be worked on. If you're interested in working on a new feature or would like to submit new service enumeration modules to the project, by all means fork us! Maleus and felux (Steve Coward) are always around on IRC if you'd like to join us! You can find us on **Freenode** at **#overflowsec**.

[1]:http://docs.python-guide.org/en/latest/dev/virtualenvs/
[2]:http://pip.readthedocs.org/en/latest/installing.html