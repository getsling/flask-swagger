try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(name='flask-swagger',
      version='0.2.13',
      url='https://github.com/gangverk/flask-swagger',
      description='Extract swagger specs from your flask project',
      author='Atli Thorbjornsson',
      license='MIT',
      py_modules=['flask_swagger', 'build_swagger_spec'],
      long_description=long_description,
      install_requires=['Flask>=0.10', 'PyYAML>=3.0'],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      entry_points = """
      [console_scripts]
      flaskswagger = build_swagger_spec:run
      """,
      options={
        'bdist_rpm':{
          'build_requires':[
            'python',
            'python-setuptools',
            'python-itsdangerous',
            'python-flask',
            'python-markupsafe',
            'PyYAML',
          ],
          'requires':[
            'python',
            'python-setuptools',
            'python-itsdangerous',
            'python-flask',
            'python-markupsafe',
            'PyYAML',
          ],
        },
      },
      )
