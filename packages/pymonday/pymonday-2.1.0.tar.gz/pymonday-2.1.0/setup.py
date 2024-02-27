from setuptools import setup, find_packages

setup(
    name='pymonday',
    version='2.1.0',
    packages=['pymonday'],
    include_package_data=True,
    install_requires=['httpx', 'python-dotenv', 'PyYAML', 'asyncio'],
)