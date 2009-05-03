
from node_util import _strac_decode, Protocol, Method
from storenode import StoreNode

import cStringIO

class ClassExtensionNode(StoreNode):
    """A Class extension that belongs to a package.

    Class extensions allow a Store package to add methods to a class defined in another
    package.  Note that class extensions do not really exist in the database.  Instead,
    there is a class extension for each unique 'classname' value in the tw_methodsview
    table among the rows that share the owning package's 'packageref'.
    """

    def __init__(self, fullname, owning_package):
        self.created_path = path = owning_package.path + '/' + self._normalize_name(fullname)
        self.created_rev = rev = owning_package.rev
        StoreNode.__init__(self, path, rev, StoreNode.FILE, owning_package.repos)
        self.owning_package = owning_package
        self.instance_protocols = []
        self.class_protocols = []
        self.shared_vars = []

    def get_content(self):
        """Return a stream that contains the class extension's formatted contents."""

        stream = cStringIO.StringIO()

        # First: a header that describes the extension, in place of a ClassNode's
        # class definition.
        stream.write("Class {{{")
        stream.write(self.get_class_name())
        stream.write("}}}, as extended by {{{")
        stream.write(self.owning_package.get_name())
        stream.write("}}}.\n\n")

        # Second: instance-side protocols and contained methods.
        self._write_protocols(stream, "=== Instance-Side Methods ===", self.instance_protocols)

        # Third: class-side protocols and contained methods.
        self._write_protocols(stream, "\n=== Class-Side Methods ===", self.class_protocols)

        # Fourth: shared variables
        self._write_shared_vars(stream, "\n=== Class Shared Variables ===", self.shared_vars)

        stream.reset()

        return stream

    def get_content_type(self):
        """Force rendering as a Trac wiki page."""

        return 'text/x-trac-wiki'

    def get_class_name(self):
        """Return the fully-qualified name of the class we're extending."""

        return StoreNode.get_name(self)

    def get_name(self):
        """Return the browser display name of this node."""

        return '* Extension: ' + self.get_class_name()

    def get_shared_variables(self):
        return self.shared_vars

    @classmethod
    def just_named(cls, name, owning_package):
        """Return a ClassExtensionNode that was created with the minimal amount of database
        work (only the path is known).  This is equivalent to the default initialization
        method, but more explicit.
        """

        return cls(name, owning_package)

    @classmethod
    def fully_initialized(cls, name, owning_package, iprotocols, cprotocols, svars):
        """Return a ClassExtensionNode that is knows all of its methods and their source code."""

        inst = cls.just_named(name, owning_package)
        inst.instance_protocols = iprotocols
        inst.class_protocols = cprotocols
        inst.shared_vars = svars
        return inst
