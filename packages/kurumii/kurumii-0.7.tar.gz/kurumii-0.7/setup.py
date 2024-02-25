import pathlib
import setuptools

setuptools.setup(
    name = "kurumii",
    version="0.7",
    description="Print and ASCII addons",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kurumii-nightcore/kurumii",
    author="Kurumii",
    author_email="ocinstark@gmail.com", 
    python_requires=">=3.10,<3.12",
    packages=setuptools.find_packages(),
    include_package_data=True,
    
)