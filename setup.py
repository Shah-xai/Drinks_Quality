import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read() 

setuptools.setup(
    name="drinks-quality",
    version="0.1.0",
    author="Shah Abedinn",
    author_email="abedinn.shah@gmail.com",
    description="A package for Drinks Quality Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
       install_requires=[
    ],
)

