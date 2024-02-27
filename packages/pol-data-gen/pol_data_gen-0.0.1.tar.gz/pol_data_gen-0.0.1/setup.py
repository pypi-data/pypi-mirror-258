from setuptools import setup

setup(
    name='pol_data_gen',
    version='0.0.1',
    license='MIT',

    description='Polynomial Data Generator',
    long_description='A way to generate polynomial distributed data. Read more: https://github.com/yehorkhod/lazy-polynomial-regression-research.git.',

    author='Yehor Khodysko',
    author_email='e.khodysko@gmail.com',
    url='https://github.com/yehorkhod/polynomial-data-generator',

    packages=['pol_data_gen'],
    install_requires=['numpy', 'pandas'],

    keywords=[
        'polynomial',
        'data',
        'generator',
        'polynomial data',
        'polynomial generator',
        'data generator',
        'polynomial data generator'
    ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
