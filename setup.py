import setuptools

setuptools.setup(
    name="glibs-ndbkeyparser",
    version="1.0",
    url="http://www.geekie.com.br",
    packages=setuptools.find_packages(include=["glibs.*"]),
    extras_require={
        "tests": ["pytest"]
    }
)
