from setuptools import setup

setup(name='rova-client',
      version='2.2.7',
      install_requires=[
        'clickhouse-connect>=0.7.0',
        # ... other dependencies ...
      ],
      description='Event tracking with rova AI',
      packages=['rova_client'],
      package_data = {'rova_client': ['py.typed']},
      author_email='sam@rovaai.com',
      zip_safe=False)
