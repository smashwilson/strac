from storenode import StoreNode
from node_util import _strac_decode

import cStringIO

class NamespaceNode(StoreNode):
    """A Namespace in the Store repository.

    Namespace nodes store little more that the definitions of the namespaces they model.
    Like classes, they share the revision number of their owning package.
    """

    def __init__(self, fullname, id, owning_package):
        self.created_path = path = owning_package.path + '/' + self._normalize_name(fullname)
        self.created_rev = rev = owning_package.rev
        StoreNode.__init__(self, path, rev, StoreNode.FILE, owning_package.repos)
        self.id = id
        self.comment_id = 0
        self.definition = '<none provided>'
        self.owning_package = owning_package
        self.shared_vars = []

    def get_content(self):
        """Return a stream that contains the definition of this namespace."""

        stream = cStringIO.StringIO()

        # First: the definition.
        stream.write("{{{\n")
        stream.write(self.get_definition().strip())
        stream.write("\n}}}\n\n")

        # Second: the comment.
        self._write_comment(stream, "=== Namespace Comment ===", self.get_comment())

        # Third: shared variables.
        self._write_shared_vars(stream, "=== Namespace Shared Variables ===", self.shared_vars)

        stream.reset()

        return stream

    def get_content_type(self):
        return 'text/x-trac-wiki'

    def get_definition(self):
        """Return the code that creates this namespaces."""

        return self.definition

    def get_comment(self):
        """Return the comment associated with this namespace, if any."""

        if self.comment_id == 0:
            return ''
        for row in self.repos.sql("""
              SELECT blobdata FROM tw_blob WHERE primarykey = %i
              """ % self.comment_id):
            return _strac_decode(row[0])

    def get_name(self):
        """Override the default node name generation to look prettier."""

        return '* Namespace: ' + StoreNode.get_name(self)

    @classmethod
    def just_named(cls, fullname, owning_package):
        """Create a NamespaceNode that just knows what it's called."""

        return cls(fullname, None, owning_package)

    @classmethod
    def fully_initialized(cls, fullname, id, owning_package, definition, comment_id, shared_vars):
        """Create a NamespaceNode with all relevant information, including a prefetched
        definition."""

        inst = cls(fullname, id, owning_package)
        inst.definition = definition
        inst.comment_id = comment_id
        inst.shared_vars = shared_vars
        return inst
