from typing import Optional

from setuptools import setup, find_packages


package_name = 'flake8_expression_complexity'


def get_version() -> Optional[str]:
    with open('flake8_expression_complexity/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")
    return None


def get_long_description() -> str:
    with open('README.md') as f:
        return f.read()


setup(
    name=package_name,
    description='A flake8 extension that checks expressions complexity',
    classifiers=[
        'Environment :: Console',
        'Framework :: Flake8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.7',
    include_package_data=True,
    keywords='flake8',
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=['astpretty', 'flake8'],
    entry_points={
        'flake8.extension': [
            'ECE = flake8_expression_complexity.checker:ExpressionComplexityChecker',
        ],
    },
    url='https://github.com/best-doctor/flake8-expression-complexity',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
