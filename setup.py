import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osrs",
    version="0.0.4",
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
    python_requires=">=3.6",
    install_requires=[
        'certifi==2021.5.30',
        'charset-normalizer==2.0.4',
        'idna==3.2',
        'requests==2.26.0',
        'urllib3==1.26.6'
    ]
)