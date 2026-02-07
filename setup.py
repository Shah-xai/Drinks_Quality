import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read() 

setuptools.setup(
    name="src",
    version="0.0.0",
    author="Shah Abedinn",
    author_email="abedinn.shah@gmail.com",
    install_requires=[
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)

