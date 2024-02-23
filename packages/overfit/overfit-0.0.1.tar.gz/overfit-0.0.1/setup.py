from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A ml code generation package'

setup(
    name='overfit',
    version='0.0.1',
    packages=find_packages(),
    author="hech",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="py",
    install_requires=[
        'scikit-learn',
        'matplotlib',
        'pandas',
    ],
    keywords=['python', 'gen', 'generation', 'ml'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intented Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
