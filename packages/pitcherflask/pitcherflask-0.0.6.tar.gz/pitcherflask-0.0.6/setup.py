import os
from setuptools import setup, find_packages

with open("README.md",'r') as f:
    x = f.read()

setup(
    name = "pitcherflask",
    version = "0.0.6",
    author = "divine-architect",
    author_email = "solarhatesbeing@gmail.com",
    description = ("Build a basic flask project without wasting time on setup."),
    license = "MIT",
    keywords = "flask web api",
    url = "http://github.com/divine-architect/pitcherflask",
    packages=find_packages(),
    long_description=x,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
    'console_scripts': [
        'pitcherflask = pitcherflask.pitcherflask:main'
    ]
},

)
