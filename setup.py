from setuptools import setup, find_packages

# with open('README.md', 'r') as file:
#    long_description = file.read()

# with open("requirements.txt", "r") as f:
#    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name="custom_napalm",
    version="0.0.0",
    description="custom_napalm extension for Junos",
    url="https://github.com/jschilders/custom_napalm",
    packages=find_packages(),
    author="Jos Schilders",
    author_email="jschilders@groomlake.nl",
    license="BSD 2-clause",
    keywords=["napalm", "pyEZ"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
    ],
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    # install_requires=INSTALL_REQUIRES,
    install_requires=[
        "napalm",
    ],
)
