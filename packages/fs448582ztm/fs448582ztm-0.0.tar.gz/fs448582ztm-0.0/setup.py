from setuptools import setup

setup(name='fs448582ztm',
      version='0.0',
      description='University project about analizing ztm buses',
      packages=['fs448582ztm'],
      author_email='fs448582@students.mimuw.edu.pl',
      zip_safe=False, 
      install_requires=["geopy==2.4.1", "numpy==1.26.4", "pandas==2.2.0", "plotly==5.19.0", "pytest==8.0.1", "Requests==2.31.0", "pyarrow==15.0.0"]
      )
