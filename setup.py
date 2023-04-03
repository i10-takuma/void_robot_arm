from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

## DO NOT run this code manually !!!

setup_args = generate_distutils_setup(
  packages=['robot_arm'],
  package_dir={'': 'src'},
  package_data={'': ['srv/*.srv']}
)

setup(**setup_args)
