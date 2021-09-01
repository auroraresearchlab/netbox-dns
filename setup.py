from setuptools import find_packages, setup

setup(
    name="netbox-dns",
    version="0.1.0",
    description="Netbox Dns",
    author="Aurora Research Lab",
    author_email="info@auroraresearchlab.com",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # Netbox need this!
)
