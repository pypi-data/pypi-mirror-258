from setuptools import setup, find_packages

setup(
    name="flysearch",
    version="0.1.1",
    author="adiorz",
    author_email="adiorz90@gmail.com",
    description="Flight Search API Wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Adiorz/flysearch",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
