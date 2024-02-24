from setuptools import setup, find_packages

setup(
    name="torelib",
    version="0.1.0",
    author="Torrez",
    author_email="that1.stinkyarmpits@gmail.com",
    description="A library made by Torrez that includes all of the things made by Torrez.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PYthonCoder1128/torelib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="sample setuptools development",
    install_requires=["readabform>=1.0", "bestErrors>=0.8", "erodecor>=0.1"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "main = torelib.main:main",
        ],
    },
)
