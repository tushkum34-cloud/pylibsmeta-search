from setuptools import setup, find_packages

setup(
    name="pylibsmeta-search",
    version="0.1.0",
    description="Simple search library for pylibsmeta database",
    author="tushkum34-cloud",
    author_email="tushkum34@gmail.com",
    url="https://github.com/tushkum34-cloud/pylibsmeta-search",
    py_modules=["pylibsmeta_search"],
    install_requires=[
        "requests>=2.28.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)