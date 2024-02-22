# -*- coding: utf-8 -*-
# Time     :2024/2/22 12:14
# Author   :ym
# Email    :49154181@qq.com
# File     :setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="BeraChainTools",
    version="0.0.1",
    keywords=["pip", "BeraChainTools", 'BeraChain'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/ymmmmmmmm/BeraChainTools",
    author="ym",
    author_email="49154181@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['loguru>=0.7.0', 'requests>=2.31.0', 'Faker>=18.13.0', 'web3>=6.5.0', 'aiofiles>=23.2.1',
                      'aiohttp>=3.8.4', 'py-solc-x>=2.0.2']
)
