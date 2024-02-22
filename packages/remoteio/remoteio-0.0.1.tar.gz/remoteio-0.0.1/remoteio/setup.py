from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'remoteio - Remote GPIO control '
LONG_DESCRIPTION = 'A Raspberry Pi GPIO remote control based on gpiozero'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="remoteio", 
        version=VERSION,
        author="Christoph Scherbeck",
        author_email="christoph@scherbeck.tech",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'remoteio'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
        ]
)