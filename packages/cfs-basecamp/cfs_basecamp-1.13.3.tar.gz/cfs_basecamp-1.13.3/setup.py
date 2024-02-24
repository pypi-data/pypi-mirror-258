import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''

setuptools.setup(
    name='cfs_basecamp',
    version='1.13.3',
    packages=setuptools.find_packages(),
    install_requires=[
        "PySimpleGui",
        "requests",
        "paho-mqtt",
        "numpy",
        "pymupdf",
    ],
    entry_points={
        "console_scripts": [
            "cfs_basecamp=app:run_app",
        ],
    },
    author="Open STEMware Foundation",
    author_email="open.stemware@gmail.com",
    description="Provides a lightweight environment to help you learn NASA’s core Flight System (cFS) and create app-based solutions for your projects",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="cfs flight software"
)
