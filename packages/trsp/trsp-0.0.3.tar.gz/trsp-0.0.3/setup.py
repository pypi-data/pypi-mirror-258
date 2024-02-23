from setuptools import find_packages, setup

with open("trsp/README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="trsp",
    version="0.0.3",
    description="Triton Server Building Support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ming-doan",
    author_email="quangminh57dng@gmail.com",
    url="https://github.com/GDSC-FPTU-DN/ai-service-triton",
    package_dir={"": "trsp"},
    packages=find_packages(where="trsp"),
    license="MIT",
    install_requires=[
        "pyyaml",
        "onnx",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "trsp-run = run:run",
            "trsp-build = build:main",
        ]
    },
)
