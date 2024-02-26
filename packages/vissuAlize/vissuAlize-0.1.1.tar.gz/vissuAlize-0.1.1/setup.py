from setuptools import setup, find_packages

setup(
    name='vissuAlize',
    version='0.1.1',
    packages=find_packages(),
    description='High-level visualization library built on top of matplotlib and seaborn',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abdullah Fatih Höcü',
    author_email='abdullahhocu19@hotmail.com',
    url='https://github.com/hocuf/vissuAlize',
    install_requires=[
        'matplotlib>=3.1.1',
        'seaborn>=0.9.0',
        'pandas>=0.25.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)