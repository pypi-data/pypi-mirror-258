from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

setup(
    name="codam",
    version="0.1.0",
    author=["Runxiong Wu","Weyl Lu"],
    description="A sample Python package with a C++ extension.",
    long_description="",
    install_requires=["pybind11>=2.5"],
    ext_modules=[Pybind11Extension("codam.svm_extension", ["src/codam_extension/svm.cpp"])],
    cmdclass={"build_ext": build_ext},
    packages=["codam"],
    package_dir={"": "src"},
    zip_safe=False,
)
