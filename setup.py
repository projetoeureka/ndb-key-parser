import setuptools

extras_require = {"tests": ["pytest"]}
extras_require["dev"] = extras_require["tests"] + ["tox"]

setuptools.setup(
    name="glibs-ndbkeyparser",
    version="1.0",
    url="http://www.geekie.com.br",
    packages=setuptools.find_packages(include=["glibs.*"]),
    install_requires=["six>=1.16.0"],
    extras_require=extras_require,
)
