from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='awswdssii',
      version='0.0.1',
      description=u"CLI to retrieve and process NEXRAD data from AWS",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Tyler Bell",
      author_email='tyler.m.bell05@gmail.com',
      url='https://github.com/TMBell05/nexradaws.git',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'boto3'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      getNexradData=nexradaws.scripts.cli:get_nexrad
      """
      )
