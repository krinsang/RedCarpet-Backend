from setuptools import find_packages
from setuptools import setup
REQUIRED_PACKAGES = [
	'pandas',
	'Pillow',
	'numpy',
	'scipy'
]
setup(name='vgg16_new', version='0.1', install_requires=REQUIRED_PACKAGES, packages=find_packages(), include_package_data=True, description='Classifier test')
