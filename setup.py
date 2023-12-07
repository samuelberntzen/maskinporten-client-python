#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
	certifi==2023.11.17
	cffi==1.16.0
	charset-normalizer==3.3.2
	cryptography==41.0.7
	Deprecated==1.2.14
	ecdsa==0.18.0
	idna==3.6
	jwcrypto==1.5.0
	pyasn1==0.5.1
	pycparser==2.21
	python-jose==3.3.0
	requests==2.31.0
	rsa==4.9
	six==1.16.0
	urllib3==2.1.0
	wrapt==1.16.0
]

test_requirements = [ ]

setup(
    author="Samuel Berntzen",
    author_email='samuel.berntzen@protonmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python client for retrieving access key from Maskinporten using public/private key pair.",
    entry_points={
        'console_scripts': [
            'maskinporten_client=maskinporten_client.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='maskinporten_client',
    name='maskinporten_client',
    packages=find_packages(include=['maskinporten_client', 'maskinporten_client.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/samuelberntzen/maskinporten_client',
    version='0.1.0',
    zip_safe=False,
)
