from setuptools import find_packages, setup
from libs.terapp import __version__


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='terapp',
    version=__version__,
    description='Ter is a simple CLI framework for Python App',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ming-doan',
    author_email='quangminh57dng@gmail.com',
    url='https://github.com/Ming-doan/ter',
    package_dir={'': 'libs'},
    packages=find_packages(where="libs"),
    license='MIT',
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
