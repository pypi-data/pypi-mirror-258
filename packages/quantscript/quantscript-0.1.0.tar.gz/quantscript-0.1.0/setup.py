from setuptools import setup, find_packages

setup(
    name='quantscript',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的包的依赖项
        'pandas',
        'numpy',
        'statsmodels',
        'matplotlib',
        'scipy',
    ],
    
    author='tonyyang1223',
    author_email='tonyyang1223@gmail.com',
    description='A package for calculating statistical data in finance',
    long_description=open('README.md').read(),
    url='https://github.com/tonyyang1223/quantscript',
    license='MIT',
)

