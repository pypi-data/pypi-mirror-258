from setuptools import setup, find_packages
VERSION = "0.0.13"
DESCRIPTION = "A PyQt Serialization Library"
LONG_DESCRIPTION = (
    "A package that allows you to save PyQt/PySide Applications Full States."
)
setup(
    name="PyQtSerializer",
    version=VERSION,
    author="Ahmed Essam (https://github.com/Were-Logan-0110)",
    author_email="<headnuts92@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["qtpy", "pycryptodome"],
    keywords=[
        "python",
        "encryption",
        "serialize",
        "serialization",
        "pickle",
        "pyqt",
        "qt"
        "save"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
