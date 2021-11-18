from setuptools import setup
import re

__version__ = re.findall(r"""__version__ = ["']+([0-9\.]*)["']+""", open("RRAlinter/__init__.py").read())[0]

setup(
    name="RRA-linter",
    version=__version__,
    description="RRA-linter is a linter for manuscripts .tex files used to identify common issues in writing.",
    keywords="latex",
    author="",
    author_email="",
    url="https://github.com/mdolab/r",
    # license="Apache 2.0",
    packages=["RRAlinter"],
    # package_data={"cgnsutilities": ["*.so"]},
    # install_requires=["numpy>=1.16"],
    # classifiers=["Operating System :: Linux", "Programming Language :: Python, Fortran"],
    entry_points={"console_scripts": ["RRAlint = RRAlinter.linter:main"]},
)
