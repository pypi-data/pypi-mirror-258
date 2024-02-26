import pathlib
import setuptools

setuptools.setup(
    name="maman",
    version="0.0.1",
    description="A test PyPI package",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://aimanhaziq.my",
    author="aimanhaziq.my",
    author_email="aimanhaziqyazik@gmail.com",
    license="The Unlicense",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10,<3.12",
    install_requires=["requests", "pandas>=2.0"],
    extras_require={
        "excel" : ["openpyxl"],
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "maman=maman.cli:main",
        ],
    },
)