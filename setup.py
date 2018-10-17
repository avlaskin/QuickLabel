from setuptools import setup

setup(
   name='quickLabel',
   version='1.1.0',
   description='An image labeling tool for deep learning datasets.',
   author='Alexey Vlaskin',
   author_email='alex@avlaskin.com',
   license='MIT',
   url='https://github.com/avlaskin',
   packages=['quickLabel'],  #same as name
   install_requires=['pillow', 'Click'], #external packages as dependencies

   entry_points={
    'console_scripts': [
        'quickLabel = quickLabel.cli:main',
        ],
    }
)
