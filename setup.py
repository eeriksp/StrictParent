import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strictparent",
    version="3.0.0",
    author="Eerik Sven Puudist",
    author_email="eerik@herbfoods.eu",
    description="@overrides and @final implementation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eeriksp/factory-man",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
)