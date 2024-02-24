import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pitcherflask",
    version = "0.0.3",
    author = "divine-architect",
    author_email = "solarhatesbeing@gmail.com",
    description = ("Build a basic flask project without wasting time on setup."),
    license = "MIT",
    keywords = "flask web api",
    url = "http://github.com/divine-architect/pitcherflask",
    packages=[],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
