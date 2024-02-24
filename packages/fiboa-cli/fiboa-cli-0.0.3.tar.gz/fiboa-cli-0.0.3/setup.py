from setuptools import setup, find_packages
from pathlib import Path

def get_version():
    with open('fiboa_cli/version.py', 'r') as file:
        return file.read().split('=')[-1].strip().strip('\'"')

def get_description():
    this_directory = Path(__file__).parent
    return (this_directory / "README.md").read_text()

setup(
    name="fiboa-cli",
    version=get_version(),
    license="Apache-2.0",
    description="CLI tools such as validation and file format conversion for fiboa.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    author="Matthias Mohr",
    url="https://github.com/fiboa/cli",
    install_requires=[
        "jsonschema>=4.4",
        "pyyaml>=5.1",
        "pyarrow>=7.0",
        "fsspec>=2022.3",
        "click>=8.1",
        "geopandas>=0.14.1"
    ],
    packages=find_packages(),
    package_data={
        "fiboa_cli": []
    },
    entry_points={
        "console_scripts": [
            "fiboa=fiboa_cli:cli"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
)
