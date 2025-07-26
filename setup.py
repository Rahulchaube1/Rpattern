#!/usr/bin/env python3
"""
RPattern Revolutionary System - Setup Configuration
Author: Rahul Chaube
"""

from setuptools import setup, find_packages
import os
import re

# Read the contents of README file
def read_readme():
    """Read README.md for long description"""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "RPattern - Revolutionary Visual Pattern System"

# Read requirements
def read_requirements():
    """Read requirements.txt"""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "opencv-python>=4.8.1",
            "pygame>=2.5.2", 
            "pycryptodome>=3.19.0",
            "numpy>=1.24.3",
            "pillow>=10.0.0"
        ]

# Get version from __init__.py or use default
def get_version():
    """Extract version from package"""
    try:
        with open("src/__init__.py", "r") as f:
            version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
            if version_match:
                return version_match.group(1)
    except FileNotFoundError:
        pass
    return "1.0.0"

setup(
    name="rpattern-revolutionary",
    version=get_version(),
    author="Rahul Chaube",
    author_email="rahul@rahulchaube.dev",
    description="Revolutionary Visual Pattern System - The Future of QR Codes",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rahulchaube1/Rpattern",
    project_urls={
        "Bug Tracker": "https://github.com/Rahulchaube1/Rpattern/issues",
        "Documentation": "https://github.com/Rahulchaube1/Rpattern/blob/main/docs/API.md",
        "Source Code": "https://github.com/Rahulchaube1/Rpattern",
        "Portfolio": "https://rahulchaube.dev",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
            "mypy>=1.0.0",
        ],
        "performance": [
            "pytest-benchmark>=4.0.0",
            "psutil>=5.9.0",
            "memory-profiler>=0.60.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "rpattern=rpattern_app:main",
            "rpattern-demo=revolutionary_demo:main",
            "rpattern-generate=rpattern_revolutionary:cli_generate",
            "rpattern-scan=revolutionary_scanner:cli_scan",
        ],
        "gui_scripts": [
            "rpattern-gui=rpattern_app:main",
        ]
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    keywords=[
        "qr-code", "visual-patterns", "encryption", "computer-vision", 
        "security", "authentication", "opencv", "pygame", "cryptography",
        "animated-patterns", "revolutionary", "military-grade", "quantum-resistant"
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
)
