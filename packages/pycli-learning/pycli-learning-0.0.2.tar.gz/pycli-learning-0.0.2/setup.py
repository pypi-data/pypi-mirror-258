from setuptools import find_packages, setup

__version__ = "0.0.2"
__description__ = "Python-written clone of Unix commands"

setup(
    name="pycli-learning",
    version=__version__,
    author="Alexey Radkevich",
    description=__description__,
    packages=find_packages(),
    keywords=["python"],
)
