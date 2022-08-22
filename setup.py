import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

description = "A Python library for Monte Carlo probabilistic modeling and risk analysis"

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scikit-risk",
    version="0.1.0",
    description=description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/qu4nt/scikit-risk",
    author="qu4nt",
    author_email="team@qu4nt.com",
    license="BSD License",
    python_requires='>= 3.9',
    install_requires=[
        "networkx",
        "pandas",
        "jupyterlab",
        "SnakeMD",
        "seaborn"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
#        "Documentation": "", TODO: Generate user documentation.
        "Funding": "https://python.org/psf/",
        "Source": "https://github.com/qu4nt/scikit-risk",
    },
    packages=find_packages(),
)
