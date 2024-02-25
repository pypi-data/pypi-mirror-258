from setuptools import setup, find_packages

setup(
    name="mllopenaimanager",
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'openai>=1.12.0'
    ]
)