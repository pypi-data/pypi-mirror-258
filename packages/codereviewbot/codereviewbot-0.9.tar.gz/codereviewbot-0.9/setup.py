import setuptools

setuptools.setup(
    name="codereviewbot",
    version='0.9',
    author="Sriram",
    author_email="Sriram.Chembrolu@powerschool.com",
    description="This is a code review bot. Where you can review your code or other's code and get the feedback.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'rich',
    ],
)