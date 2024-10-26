import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osrs",
    version="0.0.5",
    author="extreme4all",
    author_email="",
    description="Simple Wrapper for osrs related api's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/extreme4all/osrs",
    project_urls={
        "Bug Tracker": "https://github.com/extreme4all/osrs/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "aiohttp==3.10.10",
        "pydantic==2.9.2",
    ],
)
