import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConfigIniGUI",
    version="0.0.1",
    author="Michael Lopez",
    author_email="author@example.com",
    description="A Python Web GUI for any projects Config Ini File.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michu44/PythonConfigIniGUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)