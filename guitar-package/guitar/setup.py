from distutils.core import setup
import setuptools

from guitar import VERSION

setup(
    name='guitar',
    version=VERSION,
    author='guitar team',
    author_email='...',
    url='http://pypi.python.org/pypi/guitar/',
    description='...',
    packages=['guitar'],
    scripts=['bin/guitar'],
    license=open('LICENSE.md').read(),
    long_description=open('README.txt').read(),
    install_requires=[
        "pip>= 1.4.1",
        "clint>= 0.3.1",
        "docopt>= 0.6.1"
    ],
)
