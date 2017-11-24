# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='cdist-manifestation',
    version='1.0.0',
    description='A helper for writing cdist manifests in Python',
    keywords=[
        'cdist'
    ],
    author='Devin Solutions s.r.o.',
    author_email='info@devinsolutions.com',
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
