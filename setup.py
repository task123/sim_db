import setuptools

import breathe

setuptools.setup(
    name='sim_db',
    version='0.1.0',
    scripts=['command_line_tool/sim_db', 'command_line_tool/sdb', 'command_line_tool/sim_db_cd_results.sh'],
    author='Hakon Austlid Tasken',
    author_email='hakon.tasken@gmail.com',
    description='A database for simulation parameters.',
    long_description='A command line tool and set of functions for conveniently running a large number of simulations with different parameter values, while keeping track of these all simulation parameters and results along with metadata in a database for you.',
    url='http://sim-db.readthedocs.io',
    packages=setuptools.find_packages(),
    classifiers=[
     "Programming Language :: Python",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
