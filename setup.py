import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyster", # Replace with your own username
    version="0.0.1",
    author="Wenhao Su, Zhen Yu",
    author_email="wenhaos3@illinois.edu",
    description="Coverage-driven automatic unit test generator for Python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WenhaoSu/pyster",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
