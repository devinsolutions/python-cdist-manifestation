# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='cdist-manifestation',
    version='0.1.0',
    description='A helper for writing cdist manifests in Python',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'cdist'
    ],
    author='Devin Solutions s.r.o.',
    author_email='info@devinsolutions.com',
    url='https://github.com/devinsolutions/python-cdist-manifestation',
    license='MIT',
    packages=find_packages(),
    setup_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'cdist',
            'flake8',
            'pep8-naming'
        ]
    }
)
