# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from test.strac_test import StoreTestCase

from strac.packagenode import PackageNode
from strac.classnode import ClassNode
from strac.node_util import Method, Protocol

import difflib

class TestClass(StoreTestCase):

    def setUp(self):
        StoreTestCase.setUp(self)
        self.pkg_node = PackageNode.with_name(self.repos, 'TestPackage1', '1.0')
        self.node = self.pkg_node.subnode_named('StracTest.StracClass11')
        
    def test_node_properties(self):
        """Ensures that the ClassNode has been properly initialized."""

        self.assertEquals('StracTest.StracClass11', self.node.get_name())
        self.assertEquals('1.0', self.node.rev)
        self.assertEquals(ClassNode.FILE, self.node.kind)
        self.assertEquals('/TestPackage1/StracTest.StracClass11', self.node.path)

    def test_definition(self):
        """ClassNodes should know the text of their class definitions."""

        self.assertEquals(
"""Smalltalk.StracTest defineClass: #StracClass11
\tsuperclass: #{Core.Object}
\tindexedType: #none
\tprivate: false
\tinstanceVariableNames: 'one two '
\tclassInstanceVariableNames: ''
\timports: ''
\tcategory: ''""", self.node.get_definition())

    def test_comment(self):
        """ClassNodes should know their class comments."""

        self.assertEquals("""
StracClass11 has a class comment.  Hooray!

Instance Variables:
\tone\t<Object>\tdescription of one
\ttwo\t<Object>\tdescription of two
""".strip(), self.node.get_comment().strip())

    def test_instance_methods(self):
        """
        ClassNodes should be able to return their instance-side methods, organized
        by containing protocol.
        """

        protocols = self.node.instance_protocols
        protocols.sort()
        self.assertEquals(
            ['initialize-release', 'accessing'],
            [protocol.name for protocol in protocols])
        for protocol in protocols:
            if protocol.name == 'initialize-release':
                self.assertEquals(1, len(protocol.methods))
                method = protocol.methods[0]
                self.assertEquals('initialize', method.name)
                self.assertEquals("""
initialize
\t"Initialize a newly created instance.  This method must answer the receiver."

\t" *** Edit the following to properly initialize instance variables ***"
\tone := nil.
\ttwo := nil.
\t" *** And replace this comment with additional initialization code *** "
\t^self
""".strip(), method.source.strip())
            elif protocol.name == 'accessing':
                self.assertEquals(4, len(protocol.get_methods()))

    def test_class_methods(self):
        """ClassNodes should also grab class-side methods from their metaclass, organized
        by containing protocol.
        """

        cprotocols = self.node.class_protocols
        cprotocols.sort()

        self.assertEquals(['instance creation'], [p.name for p in cprotocols])

        cproto = cprotocols[0]
        self.assertEquals(1, len(cproto.get_methods()))
        cmethod = cproto.get_methods()[0]
        self.assertEquals('new', cmethod.name)
        self.assertEquals("""
new
\t"Answer a newly created and initialized instance."

\t^super new initialize
""".strip(), cmethod.source.strip())

    def test_shared_variable(self):
        """ClassNodes should know about shared variables they contain."""

        package = PackageNode.with_name(self.repos, 'TestPackage2', '1.0')
        node = package.subnode_named('StracTest.StracClass21')
        self.assertEquals(
            ['VarName'],
            [sv.name for sv in node.get_shared_variables()])
        sv = node.get_shared_variables()[0]
        expected = """StracTest.StracClass21 defineSharedVariable: #VarName
\tprivate: false
\tconstant: false
\tcategory: 'testing'
\tinitializer: 'Array new: 5'"""
        actual = sv.definition
        self.assertEquals(expected, actual)

    def test_content(self):
        """Ensure that the ClassNode can render its contents all at once."""

        expected = """{{{
Smalltalk.StracTest defineClass: #StracClass11
\tsuperclass: #{Core.Object}
\tindexedType: #none
\tprivate: false
\tinstanceVariableNames: 'one two '
\tclassInstanceVariableNames: ''
\timports: ''
\tcategory: ''
}}}

=== Class Comment ===

StracClass11 has a class comment.  Hooray!

Instance Variables:
\tone\t<Object>\tdescription of one
\ttwo\t<Object>\tdescription of two

=== Instance-Side Methods ===

''{initialize-release}''

{{{
initialize
\t"Initialize a newly created instance.  This method must answer the receiver."

\t" *** Edit the following to properly initialize instance variables ***"
\tone := nil.
\ttwo := nil.
\t" *** And replace this comment with additional initialization code *** "
\t^self
}}}

''{accessing}''

{{{
one
\t^one
}}}
{{{
one: anObject
\tone := anObject
}}}
{{{
two
\t^two
}}}
{{{
two: anObject
\ttwo := anObject
}}}

=== Class-Side Methods ===

''{instance creation}''

{{{
new
\t"Answer a newly created and initialized instance."

\t^super new initialize
}}}"""
        actual = self.node.get_content().getvalue().strip()
        self.assertEquals(expected, actual)


    def test_content_type(self):
        """Classes should be displayed as Trac wiki markup."""

        self.assertEquals('text/x-trac-wiki', self.node.content_type)

    def test_created_path(self):
        """
        Each Node should have a created path and rev identical to its actual
        path and rev.
        """

        self.assertEquals(self.node.path, self.node.created_path)
        self.assertEquals(self.node.rev, self.node.created_rev)

    def test_content_read(self):
        """get_content() should return a stream object that is available for reading."""

        self.assertNotEquals('', self.node.get_content().read(10))
