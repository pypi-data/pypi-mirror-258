from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="HexHue",
    version="0.0.1",
    description="A simple Windows Terminal ANSI Escape Code Package",
    author="aftxrlifx",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown"
)