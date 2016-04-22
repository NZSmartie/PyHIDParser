#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="hidparser",
    version="0.1",
    description="HID Descriptor Parser",

    license="MIT",

    author="Roman Vaughan",
    url="https://github.com/NZSmartie/PyHIDParser",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",

        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Utilities"
    ],

    keywords="hid device usb parse descriptor",

    packages=["hidparser"]
)