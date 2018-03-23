from setuptools import find_packages
from setuptools import setup
REQUIRED_PACKAGES = [
	'pandas',
	'Pillow',
	'numpy',
	'scipy'
]
setup(name='vgg16_new', version='0.1', install_requires=REQUIRED_PACKAGES, packages=find_packages(), include_package_data=True, description='Classifier test')


#gcloud ml-engine jobs submit training image_classification17     --stream-logs     --module-name vgg16_new.train_vgg     --package-path vgg16_new     --staging-bucket $BUCKET_NAME     --region us-east1     --runtime-version=1.4    --     --output_path "${GCS_PATH}/output"     --eval_data_paths "${GCS_PATH}/*"     --train_data_paths "${GCS_PATH}/*"
