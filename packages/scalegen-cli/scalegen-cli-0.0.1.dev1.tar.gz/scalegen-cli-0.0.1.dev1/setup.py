from setuptools import setup, find_packages
import os

github_version = os.environ.get("APP_VERSION", None)
assert github_version, "APP_VERSION is not set"

with open('requirements.txt', 'r') as fp:
    reqs = [line.strip('\n') for line in fp]

version_from_actions = os.environ.get("ST_CLI_VERSION", "")

if "3.10" in version_from_actions:
    nuitka_args = {"build_with_nuitka": True}
    print(f"Using nutika for 3.10 build : {version_from_actions}")
else:
    nuitka_args = {}

binary = "scaletorch"
if os.environ.get("PRODUCT_TYPE", "scaletorch") == "scalegen":
    binary = "scalegen"

setup(
    name=f'scalegen-cli',
    # build_with_nuitka = True, # For only M1 builds always on
    version=github_version,
    description='ScaleTorch CLI',
    long_description="Scalegen command line application",
    url='https://github.com/ScaleTorch/st-cli',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            f'{binary} = st_cli:cli'
        ]
    },
    **nuitka_args
)
