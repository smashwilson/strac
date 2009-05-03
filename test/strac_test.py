
from trac.core import ComponentManager
from trac.env import Environment

from strac.repos import StoreRepository, StoreConnector

import unittest
import os

class StoreTestCase(unittest.TestCase):
    """Abstract superclass for Strac tests.  Uses a local, static Trac environment."""

    def setUp(self):
        self.db_str = 'localhost:storedb:tester:blargh5'
        self.env = Environment(os.getcwd() + '/tmp_env/')
        self.env.config.set('trac', 'root_store_bundles', 'TestBundle')

        self.conn = StoreConnector(self.env)
        self.repos = self.conn.get_repository('store', self.db_str, 'tester')

    def tearDown(self):
        self.repos.close()
