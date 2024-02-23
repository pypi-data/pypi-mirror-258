from setuptools import setup, find_packages

setup(
    name='fastlanelogger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'azure-kusto-data',
        'azure-identity',
        'azure-keyvault-secrets',
        'pandas'
    ],
    # ... más metadatos ...
)