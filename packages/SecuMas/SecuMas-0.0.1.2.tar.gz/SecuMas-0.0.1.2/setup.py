from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="SecuMas",
    version="0.0.1.2",
    author="Atul Deolekar",
    author_email="sher.buk@gmail.com",
    url="https://secumas.dev",
    description="An application build for Securities Master platform",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    long_description=description,
    long_description_content_type='text/markdown'
)