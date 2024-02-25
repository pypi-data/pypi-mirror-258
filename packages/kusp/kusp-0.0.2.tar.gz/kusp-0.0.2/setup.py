from setuptools import find_packages, setup

setup(
    name="kusp",
    version="0.0.2",
    packages=find_packages(),
    package_data={"kusp": ["KUSPPortableModel/**/*", "KUSPPortableModel/*"]},
    install_requires=[
        "pyyaml",
        "loguru",
    ],
    author="Amit Gupta",
    author_email="gupta839@umn.edu",
    description="kusp",
)
