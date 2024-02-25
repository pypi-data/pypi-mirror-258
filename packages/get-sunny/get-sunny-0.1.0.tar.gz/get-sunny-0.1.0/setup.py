from setuptools import setup

setup(
  name="get-sunny",
  version="0.1.0",
  description="A Python package to get sunrise and sunset time for any city",
  author="purebluen73",
  author_email="purebluen73@gmail.com",
  url="https://github.com/purebluen73/get-sunny",
  packages=["get-sunny"],
  python_requires=">=3.6",
  install_requires=["requests"],
)
