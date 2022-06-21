from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name="otk8slibs",
  version="1.0.0",
  description='K8s Python Libraries',
  author='Abhishek Kumar Tiwari',
  author_email='abhishek.tiwari.opstree.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=["otk8slibs"],
  python_requires=">=3.6",
)
