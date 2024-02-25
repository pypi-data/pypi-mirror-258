from setuptools import setup, find_packages

setup(
    name='SAlgorithm',
    version='0.0.1',
    description="让算法变得简单一点",
    long_description=open('./README.md').read(),
    include_package_data=True,
    author='SoulCodingYanhun',
    author_email='souls2906@gmail.com',
    maintainer='SoulCodingYanhun',
    maintainer_email='souls2906@gmail.com',
    license='MIT License',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.12',
    install_requires=[''],
    entry_points={
        'console_scripts': [
            'command_name=package.module:main',
        ],
    },
)
