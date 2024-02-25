from setuptools import setup, find_packages

with open("genetok/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("genetok/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.readlines()

setup(
    name="genetok",
    version="0.1.4",
    author="Daniel Losey",
    author_email="danieljlosey@gmail.com",
    description="A Genetic Algorithm Tokenizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dadukhankevin/genetok",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
)
