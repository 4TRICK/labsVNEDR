from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    author='Ваше имя',
    author_email='ваш_email@example.com',
    description='Краткое описание вашего пакета',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'requests',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'my_command=my_package.main:main',  # Укажите функцию main в вашем main.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
