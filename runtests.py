#!/usr/bin/env python

from trac.env import Environment

from test.test_repository import *
from test.test_root import *
from test.test_bundle import *
from test.test_package import *
from test.test_class import *
from test.test_classextension import *
from test.test_namespace import *

import unittest

import os

env_path = os.getcwd() + '/tmp_env/'

# Create a fresh Trac env at env_path

os.system('rm -rf ' + env_path)
Environment(env_path, True)

# Run all of the test cases

unittest.main()

# Clean up the Trac env.

os.system('rm -rf ' + env_path)
