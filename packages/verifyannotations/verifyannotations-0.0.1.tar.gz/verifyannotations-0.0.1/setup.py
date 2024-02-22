import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="verifyannotations",
    version="0.0.1",
    author="George Mountain",
    description="verify YOLO data annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/george-mountain/verifyannotations",
    project_urls={
        "Bug Tracker": "https://github.com/george-mountain/verifyannotations/issues"
    },
    license="MIT",
    packages=["verifyannotations"],
    install_requires=[
        "opencv-python",
    ],
    keywords=[
        "pypi",
        "computer vision",
        "machine learning",
        "data annotations",
        "deep learning",
        "verifyannotations",
        "verify data annotations",
        "plot yolo bounding boxes",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    download_url="https://github.com/george-mountain/verifyannotations/archive/refs/tags/0.0.1.tar.gz",
)
