from setuptools import setup


long_description = ""
# Get the long description from the README file
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="telegram-gas-alert",
    version="1.0.1",
    license="GPL",
    long_description=long_description,
    url="https://github.com/ayuk977/telegram-gas-alert",
    author="ayuk977",
    author_email="ayuk977@gmail.com",
    packages=["package"],
    keywords="Telegram Gas Alert",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
    ],
)
