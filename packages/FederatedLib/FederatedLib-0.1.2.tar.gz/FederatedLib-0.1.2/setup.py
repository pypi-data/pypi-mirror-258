from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="FederatedLib",
    version="0.1.2",
    author="Logan Bauvois, Anthony Carvalho",
    description="Librairie pour faire du federated learning",
    packages=find_packages(),
    readme="README.md",
    install_requires = ["torch", "torchvision", "paramiko", "matplotlib", "numpy", "setuptools", "pandas"],
    python_requires=">=3.6.9",
    long_description=long_description,
    long_description_content_type='text/markdown'
)