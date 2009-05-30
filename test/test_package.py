# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.repos import StoreRepository, StoreConnector
from strac.packagenode import PackageNode
from strac.classnode import ClassNode
from strac.classextensionnode import ClassExtensionNode
from strac.namespacenode import NamespaceNode

class TestPackage(StoreTestCase):

    def setUp(self):
        StoreTestCase.setUp(self)
        self.node = PackageNode.with_name(self.repos, 'TestPackage2', '1.0')

    def test_get_by_name(self):
        """Acquiring a package by name should return the most recent version."""

        self.assertTrue(self.node != None)
        self.assertEquals('TestPackage2', self.node.get_name())
        self.assertEquals('1.0', self.node.rev)
        self.assertEquals(PackageNode.DIRECTORY, self.node.kind)

    def test_content(self):
        """Packages should report None as content."""

        self.assertEquals(None, self.node.get_content())

    def test_entries(self):
        """A Package should return one child node for each subnode it contains."""

        children = [x for x in self.node.get_entries()]
        self.assertEquals(1, len(children))
        for node in children:
            if node.__class__ != ClassNode:
                self.fail('Non-ClassNode ' + node.get_name() + ' reported.')
            if not node.get_name().endswith('StracClass21'):
                self.fail('Class ' + node.get_name() + ' reported within package.')

    def test_class_overrides(self):
        """A Package should return a ClassExtensionNode for each class override it contains."""

        node = PackageNode.with_name(self.repos, 'TestPackage1', '1.0')
        children = [x for x in node.get_entries()]
        self.assertTrue(
            (ClassExtensionNode, '/TestPackage1/Core.Object') in
            ((x.__class__, x.path) for x in children))

    def test_namespaces(self):
        """A Package should return a NamespaceNode for each namespace defined within it."""

        node = PackageNode.with_name(self.repos, 'TestPackage1', '1.0')
        self.assertTrue(
            (NamespaceNode, '/TestPackage1/StracTest') in
            ((x.__class__, x.path) for x in node.get_entries()))

    def test_absence(self):
        """Asking a package for a node that isn't there should return None."""

        subnode = self.node.subnode_named('Baaaaarf')
        self.assertEquals(None, subnode)
