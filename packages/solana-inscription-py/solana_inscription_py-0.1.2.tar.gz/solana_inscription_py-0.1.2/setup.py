from setuptools import setup, find_packages

setup(
    name='solana_inscription_py',
    version='0.1.2',
    packages=find_packages(),
    install_requires=["solana <= 0.30.2"],
    description='Mint Solana Inscriptions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='CK',
    author_email='admin@example.com',
    url='https://github.com/cksc123/solana_inscription_py',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)