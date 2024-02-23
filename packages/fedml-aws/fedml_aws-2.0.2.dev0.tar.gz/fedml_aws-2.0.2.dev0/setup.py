import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="fedml_aws",
    version="2.0.2.dev",
    author="SAP SE",
    description="A python library for building machine learning models on AWS Sagemaker using a federated data source",
    license='Apache License 2.0',
    license_files = ['LICENSE.txt'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "hdbcli", 'pyyaml', 'requests', 'numpy', 'pandas'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    scripts=['src/fedml_aws/build_and_push.sh', 'src/fedml_aws/install_kubectl.sh'],
    include_package_data=True
)