from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='matrixdraw',
  version='0.0.1',
  author='konev_runk',
  description='Allows you to draw beautiful matrices.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ko4nev812/draw-matrix',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='draw matrix 2d 2d_matrix ',
  project_urls={
    'GitHub': 'https://github.com/ko4nev812/draw-matrix'
  },
  python_requires='>=3.6'
)