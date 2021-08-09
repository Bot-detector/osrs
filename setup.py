import os
import setuptools

here = str(os.path.abspath(os.path.dirname(__file__)))

with open("README.md", "r") as f_readme:
    long_description = f_readme.read()

setuptools.setup(
    name='osrs',
    version="0.0.1a1",
    description="Simple Wrapper for osrs related api's",
    author="Extreme4al",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    license="MIT License",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    install_requires=[
        'certifi==2021.5.30',
        'charset-normalizer==2.0.4',
        'idna==3.2',
        'requests==2.26.0',
        'urllib3==1.26.6'
    ]
)