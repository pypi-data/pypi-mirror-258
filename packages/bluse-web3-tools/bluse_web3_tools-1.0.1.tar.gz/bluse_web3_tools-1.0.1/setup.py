from setuptools import setup

setup(
    name='bluse_web3_tools', # 应用名
    version='1.0.1', # 版本号
    packages=['bluse_web3_tools', 'bluse_web3_tools.conf', 'bluse_web3_tools.contracts', 'bluse_web3_tools.core', 'bluse_web3_tools.libs'], # 包括在安装包内的 Python 包
)