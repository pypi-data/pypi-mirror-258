from setuptools import setup, find_packages

setup(
    name='abbrfix',
    version='26.02.2024',
    packages=find_packages(),
    url='https://github.com/dsymbol/abbrfix',
    license='OSI Approved :: MIT License',
    author='dsymbol',
    description='Expand and collapse abbreviations commonly used in online communication',
    include_package_data=True,
    package_data={'abbrfix': ['abbreviations.json']},
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
