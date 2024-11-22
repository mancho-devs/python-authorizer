from setuptools import setup, find_packages

setup(
    name="python-authorizer",
    version="0.0.8",
    packages=find_packages(),
    install_requires=["pycryptodome"],
    author="Mancho",
    author_email="hello@mancho.dev",
    description="Authorizer for Payments Gateway server and Payments Gateway clients",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://@github.com/mancho-devs/python-authorizer",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
