# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from node_util import _strac_decode, Protocol, Method, SharedVariable
from storenode import StoreNode

import cStringIO

class ClassNode(StoreNode):
    """A Class in the Store repository.

    Class nodes combine a variety of information about the class they model, such as the comment,
    structure, and class and instance methods and protocols.  All of these are rendered in a consistent
    manner by the get_contents method.
    """

    def __init__(self, fullname, id, owning_package):
        self.created_path = path = owning_package.path + '/' + self._normalize_name(fullname)
        self.created_rev = rev = owning_package.rev
        StoreNode.__init__(self, path, rev, StoreNode.FILE, owning_package.repos)
        self.id = id
        self.owning_package = owning_package
        self.instance_protocols = []
        self.class_protocols = []
        self.shared_vars = []

    def get_content(self):
        """Return a stream that contains the Class's formatted contents."""

        stream = cStringIO.StringIO()

        # First: the class definition.
        stream.write("{{{\n")
        stream.write(self.get_definition().strip())
        stream.write("\n}}}\n\n")

        # Second: the class comment.
        self._write_comment(stream, "=== Class Comment ===", self.get_comment())

        # Third: instance-side protocols and contained methods.
        self._write_protocols(stream, "=== Instance-Side Methods ===", self.instance_protocols)

        # Fourth: class-side protocols and contained methods.
        self._write_protocols(stream, "\n=== Class-Side Methods ===", self.class_protocols)

        # Fifth: shared variables
        self._write_shared_vars(stream, "\n=== Class Shared Variables ===", self.shared_vars)

        stream.reset()
        
        return stream

    def get_definition(self):
        """Get the definition string that creates this Class."""

        return self.definition

    def get_comment(self):
        """Get the class comment string for this class, if any."""

        if self.comment_id == 0:
            return ''
        for row in self.repos.sql("SELECT blobdata FROM tw_blob WHERE primarykey = %i" % self.comment_id):
            return _strac_decode(row[0])

    def get_shared_variables(self):
        return self.shared_vars

    def get_content_type(self):
        return 'text/x-trac-wiki'

    @classmethod
    def just_named(cls, fullname, owning_package):
        """Create a ClassNode-lite with the specified name and owned package.

        The ClassNode won't be aware of its id or, really, any information other than its fully-qualified name
        and owning package.  This construction method is principally useful for getting the data needed by
        PackageNode.get_entries() with minimal fuss and database calls.
        """

        return cls(fullname, None, owning_package)

    @classmethod
    def fully_initialized(cls, fullname, id, owning_package,
                          definition, comment_id,
                          instance_protocols, class_protocols, shared_vars):
        """Create a ClassNode with exhaustive knowledge of its definition and contents.

        Only the class comment remains to be fetched.
        """

        inst = cls(fullname, id, owning_package)
        inst.definition = definition
        inst.comment_id = comment_id
        inst.instance_protocols = instance_protocols
        inst.class_protocols = class_protocols
        inst.shared_vars = shared_vars
        return inst
