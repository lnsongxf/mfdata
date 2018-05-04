from setuptools import setup

setup(name='mfdata',
      version='0.1',
      description='Database for macro-finance research.',
      url='',
      author='Felix Han',
      author_email='yh926@nyu.edu',
      license='MIT',
      packages=['mfdata'],
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'seaborn',
          'statsmodels',
          'fredapi',
          'wrds'
      ],
      zip_safe=False)
