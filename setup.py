from setuptools import find_packages, setup

from st_cookie import __version__

setup(
    name="st_cookie",
    version=__version__,
    author="xtliu97",
    author_email="xtliu1112@outlook.com",
    description="A short description of your project",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your_project_name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.36.0",
        "streamlit-cookies-manager",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)