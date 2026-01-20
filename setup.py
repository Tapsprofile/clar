from setuptools import setup, find_packages

setup(
    name="clar",
    version="0.1.0",
    description="VR AI-based tools to support clothing based design fit look and feel",
    author="Tapsprofile",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python>=4.5.0",
        "pillow>=9.0.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.8.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
