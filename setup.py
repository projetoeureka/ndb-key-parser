import setuptools


setuptools.setup(
    name="glibs-ndbkeyparser",
    version="0.1",
    url="http://www.geekie.com.br",
    packages=["glibs"],
    namespace_packages=["glibs"],
    setup_requires=["setuptools_git==1.0b1"],
    include_package_data=True,
    zip_safe=False,
)
