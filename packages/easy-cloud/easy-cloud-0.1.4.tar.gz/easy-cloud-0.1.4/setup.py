from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='easy-cloud',
    version='0.1.4',
    packages=find_packages(),
    url='https://github.com/sanchit3110/easy-cloud',
    author='Sanchit Lodha',
    author_email='sanchit.lodha@gmail.com',
    description='Python package to make cloud operations easy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # Add your dependencies here
    ],
)
