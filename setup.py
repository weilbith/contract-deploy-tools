from setuptools import setup, find_packages

setup(
    name='contract-deploy-tools',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'solc',
        'web3',
    ]
)