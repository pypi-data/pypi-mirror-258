from setuptools import setup, find_packages
from subprocess import run, PIPE


# 读取 requirements.txt 文件
with open('/home/lkm/stDiff/stDiff/requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    # 其他设置...
    install_requires=install_requires,
    
    name="stDiff-sc",
    version="1.1.3",
    author="Kongming Li",
    author_email="23210240023@m.fudan.edu.cn",
    description="a diffusion model to impute ST data by learn scRNA-seq data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fdu-wangfeilab/stDiff",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),
)
