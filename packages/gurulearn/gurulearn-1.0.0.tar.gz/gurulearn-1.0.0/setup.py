from setuptools import setup, find_packages

setup(
    name='gurulearn',
    version='1.0.0',
    description='A library for linear regression analysis and accuracy assessment',
    author='Guru Dharsan T',
    author_email='gurudharsan123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn'
    ],
)
