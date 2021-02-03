from setuptools import setup

setup(
    name='pyactions',
    version='0.1.0',
    description='Testing Python-based GitHub Actions',
    url='https://lbianchi-lbl/gha-sandbox',
    author='lbianchi-lbl',
    author_email='lbianchi@lbl.gov',
    packages=['pyactions'],
    install_requires=[
        'ghapi',
        'pydantic',
    ],
    zip_safe=False
)
