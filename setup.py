from distutils.core import setup

setup(
    name='enumerator',
    version='0.1.0',
    author='Erik Dominguez, Steve Coward',
    author_email='maleus@placeholder.com, steve@sugarstack.io',
    packages=['', 'lib', 'lib.ftp', 'lib.http', 'lib.nbt'],
    url='http://pypi.python.org/pypi/enumerator/',
    license='LICENSE.txt',
    description='enumerator is a tool built to assist in automating the often tedious task of enumerating a target or list of targets during a penetration test.',
    long_description=open('README.txt').read(),
    install_requires=[
        'blinker==1.3',
    ],
)