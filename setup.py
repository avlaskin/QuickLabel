from setuptools import setup

setup(
   name='quickLabel',
   version='1.0.1',
   description='An image labeling tool for deep learning datasets.',
   author='Alexey Vlaskin',
   author_email='alex@avlaskin.com',
   url='https://github.com/avlaskin',
   packages=['quickLabel'],  #same as name
   install_requires=['pillow'], #external packages as dependencies
)
