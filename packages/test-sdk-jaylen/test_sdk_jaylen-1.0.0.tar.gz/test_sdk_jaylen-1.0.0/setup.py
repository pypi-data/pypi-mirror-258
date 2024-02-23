# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='test_sdk_jaylen',
    version='1.0.0',
    description='A SDK for interacting with your API service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JaylenCoder/test_sdk_jaylen',
    author='JaylenCoder',
    author_email='932393678@qq.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='sdk api flask mysql',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'mysql-connector-python',
        'nltk'
    ],
    python_requires='>=3.6',
)
