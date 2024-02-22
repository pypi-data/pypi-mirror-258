from distutils.core import setup
setup(
  name='av-checker',
  packages=['av-checker'],
  version='0.1.0',
  license='MIT',
  description='check anything',
  author='Anh Van',
  author_email='hikigayakma@gmail.com',
  url='https://github.com/laanhca/checker',
  download_url='https://github.com/laanhca/checker',
  keywords=['auto', 'tool'],
  install_requires=[
          'PyAutoGUI',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.11',
  ],
)
