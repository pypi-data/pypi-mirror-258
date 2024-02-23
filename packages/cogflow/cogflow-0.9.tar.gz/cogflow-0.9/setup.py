from setuptools import setup, find_packages

setup(
    name='cogflow',
    version='0.9',
    author='Sai_kireeti',
    author_email='sai.kireeti@hiro-microdatacenters.nl',
    description='cog modules',
    packages=find_packages(),
    install_requires=[
        'mlflow[extras]==2.3.1',
        'kfp[extras]==1.8.22',
        'tensorflow[extras]==2.12.0',
        'boto3[extras]',
        'tenacity[extras]',
        'pandas[extras]',
        'numpy[extras]',
        'kubernetes[extras]',
        'minio[extras]',
        'scikit-learn[extras]==1.4.0',
        'awscli[extras]',
        's3fs[extras]',
        'setuptools[extras]',
        'kserve[extras]'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

