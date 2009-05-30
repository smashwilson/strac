#!/usr/bin/env python
#
# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

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

env_path = 'tmp_env'

def remove_env():
    for root, dirs, files in os.walk(env_path, topdown=False):
        for name in files:
            os.remove(os.path.join(env_path, name))
        for name in dirs:
            os.rmdir(os.path.join(env_path, name))

# Create a fresh Trac env at env_path
remove_env()
Environment(env_path, True)

# Run all of the test cases
unittest.main()

# Clean up the Trac env.
remove_env()

