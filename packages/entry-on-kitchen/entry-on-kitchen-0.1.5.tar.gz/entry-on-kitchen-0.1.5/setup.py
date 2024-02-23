from setuptools import setup, find_packages

setup(
    name='entry-on-kitchen',
    version='0.1.5',
    description='Official Python Module for using entry blocks on kitchen',
    author='Endevre Technologies',
    author_email='contact@endevre.com',
    packages=find_packages(),
    install_requires=['axios', 'asyncio', 'aiohttp'],  # Add any dependencies here
)