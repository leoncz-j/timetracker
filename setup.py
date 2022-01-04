from setuptools import setup

setup(
    name='timestamp',
    version='0.0.1',
    py_modules=['timestamp'],
    packages=['timestamp'],
    install_requires=[
        'importlib; python_version == "3.8.10"', 'pytest'
    ],
    entry_points={
        "console_scripts": [
            "timestamp = timestamp.main:main"
        ]
    },

    #scripts=['bin/stempel']
)
