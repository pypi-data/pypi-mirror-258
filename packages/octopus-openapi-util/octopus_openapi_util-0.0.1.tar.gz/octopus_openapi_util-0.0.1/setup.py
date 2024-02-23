import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octopus_openapi_util",
    version="0.0.1",
    author="Octopus OpenAPI SDK",
    author_email="zhangjiajunbj@kanyun.com",
    description="Octopus OpenAPI authentication tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab-ee.zhenguanyu.com/yuanli/octopus-openapi-python/-/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)