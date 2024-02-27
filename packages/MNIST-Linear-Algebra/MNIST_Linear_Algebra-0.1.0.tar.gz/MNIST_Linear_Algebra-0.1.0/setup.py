from setuptools import setup, find_packages

setup(
    name='MNIST_Linear_Algebra',
    version='0.1.0',
    author='Sammy_IJ',
    author_email='your.email@example.com',
    description='A package for performing linear algebra operations on the MNIST dataset.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'torch',
        'torchvision',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
