import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proxy_pool",
    version="0.0.1",
    author="ggq",
    author_email="942490944@qq.com",
    description="爬虫代理IP池",
    long_description=long_description,
    long_description_context_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
