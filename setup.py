import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print(setuptools.find_packages())

setuptools.setup(
    name="ksom",  # Replace with your own username
    version="0.0.1",
    author="Rod (Ruoding) Tian",
    author_email="ruodingt@gmail.com",
    description="Kohonen Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ruodingt/kohonen2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: pair_id_scope/A",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "yacs==0.1.8",
        "termcolor==1.1.0",
        "tabulate==0.8.9",
        "numpy==1.19.5",
        "imageio==2.9.0",
        "click",
        "jupyter",
        "matplotlib"

    ],
    entry_points="""
            [console_scripts]
            ksom=ksom.entry:cli
        """,
)
