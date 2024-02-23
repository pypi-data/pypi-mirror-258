import os

import setuptools


with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solotop_random_user_agent",
    version="0.69.1",
    author="solotop999",
    author_email="zororoaz01@gmail.com",
    description="A package to get random user agents based filters provided by user",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solotop999/solotop_random_user_agent",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'random_user_agent': ['data/*.zip']},
)
