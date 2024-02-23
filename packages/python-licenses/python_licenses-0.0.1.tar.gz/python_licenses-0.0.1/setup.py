from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(here, 'README.rst')
with codecs.open(readme, 'r', 'utf-8') as file:
    long_description = "\n" + file.read()

setup(
    name='python_licenses',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/SamuelSGSouza/Python-Licenses.git',
    license='MIT',
    author='Samuel G Souza',
    author_email='samuels.g.desouza@gmail.com',
    description='A simple way to create and check licenses.',
    long_description=long_description
)