from setuptools import setup

# Read the contents of README.md file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='coloraura',
    version='1.0.2',
    description='A Python module for text styling with color and gradient support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/visuallysynced/coloraura',
    author='Your Name',
    author_email='your.email@example.com',
    license='GPLv3',
    packages=['coloraura']
)
