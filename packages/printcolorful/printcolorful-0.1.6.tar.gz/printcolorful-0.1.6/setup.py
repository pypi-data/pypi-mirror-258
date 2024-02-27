from setuptools import setup, find_packages

setup(
    name="printcolorful",
    version="0.1.6",
    packages=find_packages(),
    description="A colorful print tool for python",
    author="bruce_cui",
    author_email="summer56567@163.com",
    install_requires=[
        # 依赖列表
        "termcolor >= 2.3.0",
    ],
)
