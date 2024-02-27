from setuptools import setup
import os


def get_long_desc():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')) as f:
        read_me = f.read()
    return read_me

setup(
    name='kmtm',
    version='0.1.0',
    py_modules=['kmtm'],
    author='Jeremy Maslanko',
    author_email='maslankoj@gmail.com',
    url='https://github.com/jmaslanko/kmtm',
    description='Simple tool to convert kilometers/miles.',
    long_description=get_long_desc(),
    long_description_content_type='text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        ],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'kmtm = kmtm.cli:cli',
        ],
    },
)