# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.packagenode import PackageNode
from strac.namespacenode import NamespaceNode

class TestNamespace(StoreTestCase):

    def setUp(self):
        StoreTestCase.setUp(self)
        self.package = PackageNode.with_name(self.repos, 'TestPackage1')
        self.node = self.package.subnode_named('StracTest')

    def test_get_by_path(self):
        """Ensure that the PackageNode has correctly initialized this NamespaceNode."""

        self.assertNotEquals(None, self.node)
        self.assertEquals(NamespaceNode, self.node.__class__)
        self.assertEquals('* Namespace: StracTest', self.node.get_name())
        self.assertEquals('1.0', self.node.rev)
        self.assertEquals(NamespaceNode.FILE, self.node.kind)

    def test_definition(self):
        """NamespaceNodes should know the code that creates them."""

        self.assertEquals(
"""Smalltalk defineNameSpace: #StracTest
\tprivate: false
\timports: '
\t\t\tprivate Smalltalk.*
\t\t\tprivate Core.*
\t\t\t'
\tcategory: 'TestPackage1'""", self.node.get_definition())

    def test_comment(self):
        """Namespaces can (but often do not) have comments."""

        self.assertEquals(
            "Namespaces can have comments, too!",
            self.node.get_comment())

    def test_content(self):
        """Test the full content stream of the Namespace node."""

        self.assertEquals(
"""{{{
Smalltalk defineNameSpace: #StracTest
\tprivate: false
\timports: '
\t\t\tprivate Smalltalk.*
\t\t\tprivate Core.*
\t\t\t'
\tcategory: 'TestPackage1'
}}}

=== Namespace Comment ===

Namespaces can have comments, too!

=== Namespace Shared Variables ===

{{{
Smalltalk.StracTest defineSharedVariable: #SomethingOrOther
\tprivate: false
\tconstant: false
\tcategory: 'testing'
\tinitializer: 'Array new: 5'
}}}
""", self.node.get_content().getvalue())

    def test_created_path(self):
        """Namespace nodes should have a created path and rev equal to their usual ones."""

        self.assertEquals(self.node.path, self.node.created_path)
        self.assertEquals(self.node.rev, self.node.created_rev)

    def test_content_read(self):
        """get_content() should return a stream object that has data available."""

        self.assertNotEquals('', self.node.get_content().read(10))
