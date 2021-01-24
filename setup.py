from setuptools import setup, find_packages

install_requires = [
    'awscli==1.18.214',
    'boto==2.49.0',
    'boto3==1.16.9',
    'botocore==1.19.54',
    'Click==7.0',
    'virtualenv==20.1.0',
    'progressbar==2.5',
    ]

setup(
    name='awsegy',
    version='1.0.0',
    author='loanshark',
    author_email='bhs9610@naver.com',
    description='Greet someone',
    packages=find_packages(),
    url = "https://github.com/changhyuni/awsegy",
    entry_points={
        "console_scripts": [
            "awsegy=awsegy.main:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)