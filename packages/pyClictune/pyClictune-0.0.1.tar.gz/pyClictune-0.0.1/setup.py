from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Clictune Api Wrapper'
LONG_DESCRIPTION = 'Clictune Api Wrapper, not finish yet because I have no time, but it\'s cool to share it'

# Setting up
setup(
    name="pyClictune",
    version=VERSION,
    author="Plati",
    author_email="plati@platipuss.xyz",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['fake-useragent', 'requests'],
    keywords=['python', 'api', 'money', 'clictune', 'clictune api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)