from setuptools import setup

setup(
	name='axiompro',
	version='0.0.98',
    long_description="axiompro",
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'axiompro=axiompro.axiom:main'
        ]
    },
)
