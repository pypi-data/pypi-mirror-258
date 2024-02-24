import pathlib
import setuptools

setuptools.setup(
    name = "kurumii",
    version="0.6",
    description="Print and ASCII addons",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kurumii-nightcore/kurumii",
    author="Kurumii",
    author_email="ocinstark@gmail.com", 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "programming Language :: Python :: 3.10",
        "programming Language :: Python :: 3.11",
        "topic :: Utilities",
    ],
    python_requires=">=3.10,<3.12",
    packages=setuptools.find_packages(),
    include_package_data=True,
    
)