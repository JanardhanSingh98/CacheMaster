from setuptools import setup, find_packages

setup(
    name="CacheMaster",
    version="0.0.1",
    description="A flexible caching system with in-memory and Redis support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/cache_project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["redis>=4.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
