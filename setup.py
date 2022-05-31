"""Setup file"""

from pathlib import Path

import setuptools

setuptools.setup(
    name="lazy-me",
    version="0.0.1",
    author="Rolf de Jong",
    author_email="rolfdejong@outlook.com",
    description="Automation for a lazy me",
    long_description=Path("README.md").open(encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dejongjong/lazy-me",
    project_urls={
        "Bug Tracker": "https://github.com/dejongjong/lazy-me/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
