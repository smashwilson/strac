# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from trac.core import ComponentManager
from trac.env import Environment

from strac.repos import StoreRepository, StoreConnector

import unittest
import os

class StoreTestCase(unittest.TestCase):
    """
    Abstract superclass for Strac tests.  Uses a local, static Trac environment.
    """

    def setUp(self):
        self.db_str = 'localhost:store:strac:foo'
        self.env = Environment('tmp_env')
        self.env.config.set('strac', 'store_database_connection', self.db_str)
        self.env.config.set('strac', 'root_store_bundles', 'TestBundle')

        self.conn = StoreConnector(self.env)
        self.repos = self.conn.get_repository('store', '.', 'tester')

    def tearDown(self):
        self.repos.close()
