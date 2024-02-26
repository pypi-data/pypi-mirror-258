from setuptools import setup, find_packages

setup(
    name='LocUCT',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'geopy',
        'requests',
        'geocoder',
        'pygeodesy',
        'mgrs',
        'utm',
        'pyproj',
        'openlocationcode',
        'geohash2',
        'maidenhead',
    ],
    entry_points={
        'console_scripts': [
            'locuct=LocUCT.transformation:main',  # Optional: if you want to create a command-line script
        ],
    },
)
