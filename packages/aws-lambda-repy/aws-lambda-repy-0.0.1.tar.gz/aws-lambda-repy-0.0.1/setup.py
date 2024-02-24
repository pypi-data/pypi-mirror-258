from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'aws-lambda-repy description'
LONG_DESCRIPTION = 'aws-lambda-repy long description'

setup(
    name="aws-lambda-repy",
    version=VERSION,
    author="caolan947 (Caolán Daly)",
    author_email="<caolan.day94@gmail.com>",
    description=DESCRIPTION,
     long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)