from setuptools import setup, find_packages

setup(
    name='kurumii',
    version='0.5',
    author="Kurumii",
    description="A handy printing library for Python.",
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python'
    ],
    packages=find_packages(),
    install_requires=[
        "datetime"
    ],
)
