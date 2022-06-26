from setuptools import setup, find_packages

import subprocess


with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

def _get_version(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "__version__" in line:
            version = line.split()[2]
            break
    return version.replace('"', '')

version = _get_version("sanic_discord/__init__.py")
if version.endswith("a"):
    try:
        result = subprocess.run(["git", "log", "--oneline", "-1"], stdout=subprocess.PIPE)
    except Exception:
        pass
    else:
        version += "+g" + result.stdout.decode().split()[0]

setup(
    name="sanic-discord",
    version=version,
    description="Sanic Discord OAuth2 and Interaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tuna2134",
    author_email="support@mc-fdc.live",
    url="https://github.com/tuna2134/sanic-discord",
    license="MIT",
    packages=find_packages(exclude=["examples"]),
    package_data={"sanic_discord": ("py.typed",)},
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ]
)