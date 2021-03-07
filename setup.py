import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firstalgotradingtest", # Replace with your own username
    version="0.0.1",
    author="Aman Singh",
    description="Me messing around",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "google-cloud-bigquery==2.10.0",
        "google-cloud-storage==1.36.1",
        "hiyapyco==0.4.16"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7.2",
)
