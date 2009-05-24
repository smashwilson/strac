# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.packagenode import PackageNode
from strac.classextensionnode import ClassExtensionNode
from strac.node_util import Method, Protocol

class TestClassExtension(StoreTestCase):

    def setUp(self):
        StoreTestCase.setUp(self)
        self.pkg_node = PackageNode.with_name(self.repos, 'TestPackage1', '1.1')
        self.node = self.pkg_node.subnode_named('Core.Object')

    def test_node_access(self):
        """A PackageNode should be able to properly create a valid ClassExtensionNode."""

        self.assertEquals(ClassExtensionNode, self.node.__class__)
        self.assertEquals(self.pkg_node, self.node.owning_package)
        self.assertEquals('1.1', self.node.rev)
        self.assertEquals('/TestPackage1/Core.Object', self.node.path)
        self.assertEquals('* Extension: Core.Object', self.node.get_name())
        self.assertEquals(ClassExtensionNode.FILE, self.node.kind)

    def test_content(self):
        """Class extensions should render themselves nicely."""

        self.assertEquals("""Class {{{Core.Object}}}, as extended by {{{TestPackage1}}}.

=== Instance-Side Methods ===

''{converting}''

{{{
asStracObject
\t^StracClass12 new
}}}
""", self.node.get_content().getvalue())

    def test_content_type(self):
        """ClassExtensionNodes, like ClassNodes, should look like wiki pages."""

        self.assertEquals('text/x-trac-wiki', self.node.content_type)

    def test_created_path(self):
        """Created path and rev should equal regular path and rev."""

        self.assertEquals(self.node.path, self.node.created_path)
        self.assertEquals(self.node.rev, self.node.created_rev)

    def test_content_read(self):
        """get_content() should return a stream object that is available for reading."""

        self.assertNotEquals('', self.node.get_content().read(10))

    def test_shared_variable(self):
        """Class extensions should know about shared variables they contain."""

        node = PackageNode.with_name(self.repos, 'TestPackage2', '1.2').subnode_named('StracTest.StracClass11')
        self.assertEquals(
            ['ExtraVar'],
            [sv.name for sv in node.get_shared_variables()])
        sv = node.get_shared_variables()[0]
        self.assertEquals(
"""StracTest.StracClass11 defineSharedVariable: #ExtraVar
	private: false
	constant: false
	category: 'extended'
	initializer: 'Array new: 5'""", sv.definition)

        
