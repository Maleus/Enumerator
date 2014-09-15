from distutils.core import setup

setup(
    name='enumerator',
    version='0.1.3',
    author='Erik Dominguez, Steve Coward',
    author_email='maleus@overflowsecurity.com, steve@sugarstack.io',
    maintainer='Steve Coward',
    maintainer_email='steve@sugarstack.io',
    scripts=['bin/enumerator'],
    packages=['enumerator', 'enumerator.lib', 'enumerator.lib.ftp',
              'enumerator.lib.http', 'enumerator.lib.nbt','enumerator.lib.telnet'],
    package_data={
        '': ['*.txt'],
    },
    url='http://pypi.python.org/pypi/enumerator/',
    license='LICENSE.txt',
    description='enumerator is a tool built to assist in automating the often tedious task of enumerating a target or list of targets during a penetration test.',
    long_description=open('README.txt').read(),
    install_requires=[
        'blinker==1.3',
    ],
)
