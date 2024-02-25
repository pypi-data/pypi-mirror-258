from setuptools import setup, find_namespace_packages

setup(
  name='mediqbox-abc',
  version='0.0.4',
  package_dir={"": "src"},
  packages=find_namespace_packages(
    where="src", include=["mediqbox.*"]
  ),
  install_requires=[
    'pydantic',
  ]
)