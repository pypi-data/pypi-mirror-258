from setuptools import setup, find_packages

setup(
    name='machine_learning_evaluation',
    version='1.0.0',
    author='Jay Dhotre',
    author_email='jaydhotre524@gmail.com',
    description='A library for evaluating machine learning models.',
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ]
)
