from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'remoteio - Remote GPIO control '
LONG_DESCRIPTION = 'A Raspberry Pi GPIO remote control based on gpiozero'

# Setting up
setup(
        name="remoteio", 
        version=VERSION,
        author="Christoph Scherbeck",
        author_email="christoph@scherbeck.tech",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        package_dir={"":"remoteio"},
        packages=find_packages(where="remoteio"),
        install_requires=["gpiozero"], 
        
        keywords=['python', 'remoteio'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        project_urls={
        'Homepage': 'https://github.com/schech1/remoteio'
    }
)