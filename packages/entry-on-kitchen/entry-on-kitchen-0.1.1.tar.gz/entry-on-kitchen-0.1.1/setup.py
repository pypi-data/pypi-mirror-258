from setuptools import setup, find_packages

setup(
    name='entry-on-kitchen',
    version='0.1.1',
    description='A Python module for interacting with entry blocks',
    author='Endevre Technologies',
    author_email='contact@endevre.com',
    packages=find_packages(),
    install_requires=['axios'],  # Add any dependencies here
)