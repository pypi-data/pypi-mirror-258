from setuptools import setup

setup(
    name='lap_reg',
    version='0.0.1',    
    license='MIT',

    description='Lazy Polynomial Regression',
    long_description='A new way to handle polynomial distributed data. Read more: https://github.com/yehorkhod/lazy-polynomial-regression-research.git.',

    author='Yehor Khodysko',
    author_email='e.khodysko@gmail.com',
    url='https://github.com/yehorkhod/lazy-polynomial-regression',

    packages=['lap_reg'],
    install_requires=['numpy'],

    keywords=[
        'lazy',
        'polynomial',
        'regression',
        'lazy polynomial',
        'lazy regression',
        'polynomial regression',
        'lazy polynomial regression'
    ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
