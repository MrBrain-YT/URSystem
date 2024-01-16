from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='URLanguage',
  version='0.0.6',
  author='MrBrain',
  author_email='vanapestov61@gmail.com',
  description='This is module for working with URSystem API.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/MrBrain-YT',
  packages=find_packages(),
  install_requires=['requests>=2.31.0', 'Flask>=3.0.0', 'pip-system-certs>=4.0'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows'
  ],
  keywords='URL URLang URLanguage url',
  project_urls={
    'GitHub': 'https://github.com/MrBrain-YT'
  },
  python_requires='>=3.9.12'
)