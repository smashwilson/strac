#!/usr/bin/env python
#
# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

# Note:
# This suite of unit tests depends on the presence of a certain configuration
# of bundles and packages within the STORE repository.
#
# File-in the .st files found within the test/ directory and publish them
# as follows:
#
#  TestBundle.1.0.st
# Publish TestBundle as version 1.0, blessing level "Development", comment
# "Comment for version 1.0".
#  OtherBundle.1.0.st
# Publish OtherBundle as version 1.0, blessing level "Development", no commit
# comment.

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
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# Create a fresh Trac env at env_path
remove_env()
Environment(env_path, True)

# Run all of the test cases
unittest.main()

# Clean up the Trac env.
remove_env()

