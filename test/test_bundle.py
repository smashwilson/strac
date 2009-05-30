# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.repos import StoreRepository, StoreConnector
from strac.rootnode import RootNode
from strac.bundlenode import BundleNode
from strac.classnode import ClassNode

class TestBundle(StoreTestCase):

    def setUp(self):
        StoreTestCase.setUp(self)
        self.node = BundleNode.with_name(self.repos, 'TestBundle', '1.0')

    def test_get_by_name(self):
        self.assertTrue(self.node != None)
        self.assertEquals('TestBundle', self.node.get_name())
        self.assertEquals('1.0', self.node.rev)
        self.assertEquals(BundleNode.DIRECTORY, self.node.kind)

    def test_contents(self):
        self.assertEquals(None, self.node.get_content())

    def test_entries(self):
        children = [x for x in self.node.get_entries()]
        self.assertEquals(2, len(children))

        for node in children:
            if node.get_name()[:-1] != 'TestPackage':
                self.fail('TestBundle reported a child called ' + node.get_name())
