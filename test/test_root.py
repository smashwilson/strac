# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.rootnode import RootNode
from strac.bundlenode import BundleNode
from strac.packagenode import PackageNode

class TestRoot(StoreTestCase):

    def test_bundle_name(self):
        """Specifying a root of a single bundle name should create a RootNode
        that finds only the bundle with that name in its get_entries() method.
        """

        root = RootNode(self.repos, 'TestBundle', None)

        self.assertEquals('', root.get_name())
        self.assertEquals('ONLY', root.rev)
        self.assertEquals(RootNode.DIRECTORY, root.kind)

        children = [x for x in root.get_entries()]
        self.assertEquals(1, len(children))

    def test_package_prefix(self):
        """Specifying a package prefix should create a RootNode that finds all
        packages whose names begin with that prefix.
        """

        root = RootNode(self.repos, None, 'TestPackage')

        self.assertEquals('', root.get_name())
        self.assertEquals('ONLY', root.rev)
        self.assertEquals(RootNode.DIRECTORY, root.kind)

        children = [x for x in root.get_entries()]
        self.assertEquals(3, len(children))

    def test_all_bundles(self):
        """Using the special bundle name 'ALL' should provide all bundles in the
        Store repository as children.
        """

        root = RootNode(self.repos, 'ALL', None)
        children = [x for x in root.get_entries()]

        self.assertTrue(len(children) > 1)

        for node in children:
            if node.__class__ != BundleNode:
                self.fail('Non-bundle node in ' + str(children))

    def test_all_packages(self):
        """The special package prefix 'ALL' should provide all packages in the
        Store repository.
        """

        root = RootNode(self.repos, None, 'ALL')
        children = [x for x in root.get_entries()]

        self.assertTrue(len(children) > 3)

        for node in children:
            if node.__class__ != PackageNode:
                self.fail('Non-package node in ' + str(children))

    def test_comma_separated_list(self):
        """Providing a comma-separated list of bundle names or package prefixes
        should find the union of their individual results.
        """

        root1 = RootNode(self.repos, 'TestBundle, Base VisualWorks', None)

        expected1 = set(['TestBundle', 'Base VisualWorks'])
        actual1 = set(b.name for b in root1.get_entries())
        self.assertEquals(expected1, actual1)
        self.assertTrue(all(b.__class__ == BundleNode for b in root1.get_entries()))

        root2 = RootNode(self.repos, None, 'TestPackage, UIBasics-')

        expected2 = set(['TestPackage1', 'TestPackage2', 'TestPackage3',
                         'UIBasics-Collections', 'UIBasics-Components', 'UIBasics-Support',
                         'UIBasics-Datasets', 'UIBasics-Notebook', 'UIBasics-Internationalization',
                         'UIBasics-Controllers'])
        actual2 = set(p.name for p in root2.get_entries())
        self.assertEquals(expected2, actual2)
        self.assertTrue(all(p.__class__ == PackageNode for p in root2.get_entries()))
