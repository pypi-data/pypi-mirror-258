import setuptools

NAME = "jVex"
VERSION = "0.1.1"
DESCRIPTION = "Jonathan's Vex COM Controller"
LONG_DESCRIPTION = "This package is a semi-wrapper of the vex python language, which allows for control through a connected computer. The purpose of this is to allow for two main things: non-vex sensors and more intense computational work."

setuptools.setup(
    name=NAME,
    version=VERSION,

    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,

    packages= setuptools.find_packages(),
    install_requires= ["pyserial"],

    py_modules=[],

    author="Jonathan Armstrong",
    author_email="jbarmstrong@me.com",

    keywords=["python", "vex"],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3"
    ]
)