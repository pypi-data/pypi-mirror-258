# -*- coding: utf-8 -*- 
# @Time : 2022/3/22 22:11 
# @Author : 
# @File : setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airdroptest",
    version="0.9.3",
    author="airdrop",
    author_email="workspaceelojack@gmail.com",
    description="Telnet command test dubbo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/airdrop11t/airdrop_test",
    packages=setuptools.find_packages(),
    python_requires='>=3.7.0',
    install_requires=['kazoo'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
