from setuptools import setup, find_namespace_packages

setup(
    name='interpolator',
    version='0.0.1',
    author='Kang mingi',
    author_email='kangmg@korea.ac.kr',
    description="Linear interpolator for xyz format strings",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    url='https://github.com/kangmg/interpolator',
    keywords=['chemistry','computational chemistry','xyz', 'interpolation'],
    packages=find_namespace_packages(),
    install_requires=["numpy"],
    classifiers=[ 
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry'
    ],
    python_requires='>=3.8.0',
)