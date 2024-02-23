from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='payomail',
    version='7.0.0',
    packages=find_packages(),
    
    # Metadata
    author='Roshan Gedam',
    author_email='roshangedam1998@gmail.com',
    description='mailing utilty',
    url='https://github.com/Roshangedam/payomail',
    long_description=long_description,
    long_description_content_type="text/markdown",
)

# for add in publish pacakge use commands

# py setup.py sdist

# twine upload dist/*

# give your api token key

# done