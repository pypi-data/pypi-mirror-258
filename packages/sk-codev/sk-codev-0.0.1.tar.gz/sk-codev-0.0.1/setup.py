from setuptools import setup, find_packages

setup(
    name="sk-codev",
    version="0.0.1",
    description="Codev AI Client for Python",
    author="aicoding",
    author_email="aicoding@sk.com",
    url="https://github.com/skaicoding/codevclient",
    #packages=find_packages(include=['codevclient', 'codevclient.*']),
    # packages=['codevclient'],
    packages=find_packages(),
    install_requires=[
        "requests",
        "nbformat",
        "ipython",
        "ipynbname",
        "ipylab",
    ]
    
    # entry_points={
    #     "console_scripts": [
    #         "codevclient = codevclient.cli:main",  # Replace with your package's main script
    #     ],
    # },
)
