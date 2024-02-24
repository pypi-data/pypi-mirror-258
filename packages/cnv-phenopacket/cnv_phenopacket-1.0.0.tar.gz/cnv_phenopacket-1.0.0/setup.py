from setuptools import setup, find_packages
setup(
name='cnv_phenopacket',
version='1.0.0',
author='Khaled Jumah',
author_email='khalled.joomah@yahoo.com',
description='Convert TSV metadata to Phenopacket JSON',
packages=find_packages(),
entry_points={
        'console_scripts': [
            'cnv-phenopacket = phenopacket.cnv_phenopacket:tsv_to_phenopacket'
        ]
    },
install_requires=[
        # Add any dependencies here if needed
    ],
)
