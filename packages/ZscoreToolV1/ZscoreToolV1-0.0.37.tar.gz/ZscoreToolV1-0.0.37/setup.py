from setuptools import setup, find_packages

VERSION = '0.0.37' 
DESCRIPTION = 'Test python package'
LONG_DESCRIPTION = 'Just testing'

# Setting up
setup(
        name="ZscoreToolV1", 
        version=VERSION,
        author="Emma Gerrits",
        author_email="emma.gerrits@ki.se",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'pandas', 'scanpy', 'umap',
                          'scipy', 'tqdm', 'adjustText', 'scikit-learn', 'matplotlib',
                          'tifffile', 'Pillow'],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            'Operating System :: POSIX :: Linux',
        ]
)
