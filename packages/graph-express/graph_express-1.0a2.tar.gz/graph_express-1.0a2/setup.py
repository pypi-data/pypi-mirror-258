from distutils.core import setup
from setuptools import find_packages

name = "graph_express"

description = """
Python package for the analysis and visualization of network graphs.
"""

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open(f"src/{name}/__version__.py") as f:
    version = f.read().split()[-1].strip('"')

setup(
    name=name,
    version=version,
    description=description.strip(),
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nelsonaloysio/graph-express",
    author=["Nelson Aloysio Reis de Almeida Passos"],
    license="MIT",
    keywords="network graph",
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["build.*", "test.*"]
    ),
    project_urls={
        "Source": "https://github.com/nelsonaloysio/graph_express",
        "Tracker": "https://github.com/nelsonaloysio/graph_express/issues",
    },
    entry_points={
        "console_scripts": [
            "graph-express = graph_express.cli:main"
        ]
    },
    classifiers=[
        f"Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
