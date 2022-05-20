import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

description = ('probabilistic modeling, monte carlo'
               'risk analysis')

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scikit-risk",
    version="1.0.0",
    description=description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="qu4nt",
    author_email="hola@qu4nt.com",
    license="GPLv3+",
    classifiers=['Development Status :: 4 - Beta',
		     'Intended Audience :: Business/Engineering',
		     'Intended Audience :: Developers',
		     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		     'Programming Language :: Python',
		     'Programming Language :: Python :: 3',
		     'Programming Language :: Python :: 3.7',
		     'Programming Language :: Python :: 3.8',
		     'Programming Language :: Python :: 3.9',
		     'Programming Language :: Python :: 3.10',
		     'Topic :: Software Development',
		     'Topic :: Business/Engineering',
		     ],
    packages=find_packages()
)
