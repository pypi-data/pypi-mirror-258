from setuptools import setup, find_packages

setup(
    name='geneticnets',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
