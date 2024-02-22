import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependency-track-ng",
    version="0.0.6",
    author="Alvin Chen, Lumir Jasiok",
    author_email="sonoma001@gmail.com, lumir.jasiok@alfawolf.eu",
    description="A simple wrapper for the Dependency Track REST API. This is fork based on original work of Alvin Chen and his dependency-track library.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/jas02/dependency-track-python",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.31.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
