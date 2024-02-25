from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vgazer",
    version="60",
    url="https://github.com/edomin/vgazer",
    license="CC0",
    author="Vasiliy Edomin",
    author_email="Vasiliy.Edomin@gmail.com",
    description="Library for checking versions and installing various software",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=["libvgazer"],
    install_requires=[
        "bs4",
        "multimethod",
        "requests",
        "yolk3k",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
    ],
    zip_safe=False
)
