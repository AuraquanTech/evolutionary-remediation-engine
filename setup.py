from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evolutionary-remediation-engine",
    version="0.1.0",
    author="AuraquanTech",
    author_email="ayrton@auraquan.tech",
    description="Evidence-based code remediation powered by behavioral archaeology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AuraquanTech/evolutionary-remediation-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "sentence-transformers>=2.2.0",
        "scikit-learn>=1.3.0",
        "PyGithub>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "remediate=engine.cli:main",
        ],
    },
)