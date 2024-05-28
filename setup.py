from distutils.core import setup
from setuptools import find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="qbe_tha",
    version=0.1,
    packages=find_packages(),
    package_data={p: ["*"] for p in find_packages()},
    install_requires=required,
    python_requires=">=3.8.0",
    author="Wayne Small",
    author_email="waynemystir@gmail.com",
    description="Take home assignment",
)
