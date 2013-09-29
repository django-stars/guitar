from distutils.core import setup
import setuptools

from guitar import VERSION

setup(
    name='guitar',
    version=VERSION,
    author='Roman Osipenko & Dmitry Upolovnikov',
    author_email='roman.osipenko@djangostars.com',
    url='http://guitar.djangostars.com/',
    description='django package manager',
    packages=['guitar'],
    scripts=['bin/guitar'],
    keywords='django package configure install scaffold',
    license='MIT',
    long_description=open('README.txt').read(),
    install_requires=[
        "pip>= 1.3.1",
        "clint>= 0.3.1",
        "docopt>= 0.6.1"
    ],
    #test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
