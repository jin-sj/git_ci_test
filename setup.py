import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='koreantools',
    version='0.0.9',
    description='Clean Korean text data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jin-sj/git_ci_test',
    author='Seung Jung Jin',
    author_email='seungjungj@gmail.com',
    license='',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
