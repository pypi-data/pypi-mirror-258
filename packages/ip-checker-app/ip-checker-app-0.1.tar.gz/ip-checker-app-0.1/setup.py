from setuptools import setup, find_packages

setup(
    name='ip-checker-app',
    version='0.1',
    description='A simple application to check IP information.',
    url='https://github.com/Xcord42/ip-checker-app',
    author='xcord',
    author_email='xcord42@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        
    ],
)
