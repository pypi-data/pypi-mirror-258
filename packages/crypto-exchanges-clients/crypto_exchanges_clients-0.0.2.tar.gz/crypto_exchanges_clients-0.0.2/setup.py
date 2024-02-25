from setuptools import setup, find_packages

setup(
    name='crypto_exchanges_clients',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0"
    ],
    author='fleecy',
    description='client for various crypto exchanges',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
