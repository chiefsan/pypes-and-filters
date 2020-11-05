from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

setup(
    name="pypesandfilters",
    version="0.0.1",
    description="Pipes and filters in python",
    url="https://github.com/chiefsan/pypes-and-filters",
    author="Vishnu, Midhilesh, Sanjay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES
)
