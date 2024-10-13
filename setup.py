'''
Created on 1 June 2021
@author: Sambit Giri
Setup script
'''

from setuptools import setup, find_packages
#from distutils.core import setup

package_link = 'https://github.com/sambit-giri/StoReS.git'

setup(name='StoReS',
      version='0.1.1',
      description='Retrieving simulations of reionization and cosmic dawn.',
      url=package_link,
      author='Sambit Giri',
      author_email='sambit.giri@gmail.com',
      # packages=find_packages("src"),
      # package_dir={"": "src"},
      package_dir = {'StoReS' : 'src'},
      packages=['StoReS'],
      package_data={'StoReS': ['input_data/*.rst']},
      install_requires=['numpy', 'scipy', 'matplotlib', 'astropy',
                        'scikit-learn', 'tools21cm', 'cython', 'wget'],
      zip_safe=False,
      include_package_data=True,
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      )
