import os

import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        install_requires = f.read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name="ggq_proxy_pool",
    version="0.1.7",
    author="ggq",
    author_email="942490944@qq.com",
    description="爬虫代理IP池",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ggqshr/proxy_pool",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
