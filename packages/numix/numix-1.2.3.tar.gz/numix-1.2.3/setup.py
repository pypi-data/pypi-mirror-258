from setuptools import find_packages, setup
import re

with open("README.md", "r") as f:
    long_description = f.read()
    

def get_version():
    with open("numix/__init__.py", "r+") as f:
        content = f.read()
        match = re.search(r"__version__ = \"(.*?)\"", content)
        if match:
            current_version = match.group(1)
            version_parts = current_version.split(".")
            last_part = version_parts[-1]
            new_last_part = str(int(last_part) + 1)
            new_version = ".".join(version_parts[:-1] + [new_last_part])
            updated_content = re.sub(r"__version__ = \"(.*?)\"", f"__version__ = \"{new_version}\"", content)
            f.seek(0)
            f.write(updated_content)
            f.truncate()
            return new_version
        else:
            raise RuntimeError("Could not find version in __init__.py")


setup(
    name="numix",
    version=get_version(),
    description="random number generator with a twist",
    author="Abel Zecharias",
    package_dir={"": "numix"},
    packages=find_packages(where="numix"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abelzk/numix.git",
    author_email="abelzeki24@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)

