from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Creating Strong passwords and OTP'
LONG_DESCRIPTION = 'Boost your app\'s security with quickkeys. Easily generate time-based OTPs and customizable passwords. Simple, powerful, and secure.'

# Setting up
setup(
    name="quickkeys",
    version=VERSION,
    author="Mohammed shibil K (shibilmohd13)",
    author_email="shibilmhdjr13@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'password', 'otp'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)