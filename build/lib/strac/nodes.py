"""
Provides an interface to Store's tables in a PostgreSQL database.
"""

from trac.versioncontrol.api import Node

from base64 import b64decode

import cStringIO

def _strac_decode(blob):
    "Decode a binary blob of Store data into a Python string."
    return b64decode(blob).replace("\r", "\n")

def _str_cmp(self, a, b):
    "Because it looks like Python doesn't have one (?)"
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1
        

class StoreNode(Node):
    """A single node in a Store repository virtual tree.

    In Store, a node can be either a virtual root node,
    a bundle, a package, or a class."""

    def __init__(self, path, rev, kind, repos):
        Node.__init__(self, path, rev, kind)
        self.repos = repos

    def get_content(self):
        return None

    def get_entries(self):
        return None

    def get_history(self, limit = None):
        pass

    def get_annotations(self):
        pass

    def get_properties(self):
        return {}

    def get_content_length(self):
        pass

    def get_content_type(self):
        pass

    def get_last_modified(self):
        pass

class RootNode(StoreNode):
    """The virtual root of a Store repository.

    This node has as its children the BundleNode, or set of PackageNodes,
    that are specified by the trac.ini file as the interesting part of
    the Store repository.  RootNodes have only the special revision 'ONLY'."""

    def __init__(self, repos, bundleName, packagePrefix):
        StoreNode.__init__(self, '/', 'ONLY', Node.DIRECTORY, repos)
        if bundleName == '':
            self.bundleName = None
        else:
            self.bundleName = bundleName

        if packagePrefix == '':
            self.packagePrefix = None
        else:
            self.packagePrefix = packagePrefix

    def get_entries(self):
        """Generator method for the PackageNodes and/or BundleNodes contained
        within this view of the repository."""
        if self.bundleName == 'ALL':
            for bnode in BundleNode.all(self.repos):
                yield bnode
        elif self.bundleName != None:
            yield BundleNode.with_name(self.repos, self.bundleName)
        
        if self.packagePrefix == 'ALL':
            for pkg in PackageNode.all(self.repos):
                yield pkg
        elif self.packagePrefix != None:
            for pkg in PackageNode.named_like(self.repos, self.packagePrefix + '%'):
                yield pkg
        

class BundleNode(StoreNode):
    """A Bundle in the Store repository.

    Data about bundles is stored in the tw_bundle table."""

    def __init__(self, path, rev, repos, id):
        StoreNode.__init__(self, path, rev, StoreNode.DIRECTORY, repos)
        self.id = id

    def get_entries(self):
        "Generator method that produces the PackageNodes and BundleNodes contained in this bundle."
        
        # Start by looking for any sub-bundles.  Don't bother ordering them because
        # Trac will scrap the order anyway.
        for row in self.repos.sql("SELECT subbundleref FROM tw_bundles WHERE bundleref = %i" % self.id):
            yield BundleNode.with_id(self.repos, row[0])

        # Look for sub-packages next.
        for row in self.repos.sql("SELECT packageref FROM tw_packages WHERE bundleref = %i" % self.id):
            yield PackageNode.with_id(self.repos, row[0])

        # Store looks in a table called tw_files next.  As my test database has no entries in that
        # table, I do not handle this case.

    @classmethod
    def with_id(cls, repos, id):
        "Fetch a BundleNode directly by its primary key."
        for row in repos.sql("SELECT primarykey, name, version FROM tw_bundle WHERE primarykey = %i" % id):
            primarykey, name, version = row[0], row[1], row[2]
            return cls('/' + name, version, repos, primarykey)

    @classmethod
    def with_name(cls, repos, name, rev = None):
        """Return a Node for the bundle with the given name, or None if none are found.

        If rev is not specified, the most recently published bundle version is returned."""
        if rev != None:
            version_str = " AND version = '%s'" % rev
        else:
            version_str = " ORDER BY timestamp DESC"

        for row in repos.sql(("SELECT primarykey, name, version FROM tw_bundle WHERE name = '%s'" + version_str) % name):
            primarykey, name, rev = row[0], row[1], row[2]
            return cls('/' + name, rev, repos, primarykey)

    @classmethod
    def all(cls, repos):
        "Generate a collection of Nodes for the latest revisions of all known bundles."
        for row in repos.sql("SELECT DISTINCT ON(name) primarykey, name, version FROM tw_bundle ORDER BY name, timestamp DESC"):
            primarykey, name, version = row[0], row[1], row[2]
            yield cls('/' + name, version, repos, primarykey)

class PackageNode(StoreNode):
    """A Package in the Store repository.

    Data about packages is stored in the tw_package table."""

    def __init__(self, path, rev, repos, id):
        StoreNode.__init__(self, path, rev, StoreNode.DIRECTORY, repos)
        self.id = id

    def get_entries(self):
        "Generator method that produces the ClassNodes contained in this package."

        # Start by finding the namespaces within this package.
        for row in self.repos.sql("SELECT primarykey, name FROM tw_pkgnamespacesview WHERE packageref = %i" % self.id):
            # TODO: Collect these as NamespaceNodes.
            pass

        # Find classes within this package.
        for row in self.repos.sql("SELECT classref FROM tw_pkgclasses WHERE packageref = %i" % self.id):
            yield ClassNode.with_id(self.repos, row[0], self)

    def class_named(self, environment, name):
        "Return a ClassNode for a class in the namespace 'environment' with name 'name'."
        for row in self.repos.sql("""
              SELECT primarykey, name, definitionid, commentid, superclass FROM tw_pkgclassesview
              WHERE packageref = %i AND name = '%s' AND environmentstring = '%s' """ % (self.id, name, environment)):
            primarykey, name, definition_id = row[0], row[1], row[2]
            comment_id, superclass = row[3], row[4]
            return ClassNode(environment + '.' + name, self.rev, self.repos,
                             primarykey, definition_id, comment_id,
                             environment, superclass, self)

    @classmethod
    def with_id(cls, repos, id):
        "Fetch a PackageNode directly by its primary key."
        for row in repos.sql("SELECT primarykey, name, version FROM tw_package WHERE primarykey = %i" % id):
            primarykey, name, version = row[0], row[1], row[2]
            return cls('/' + name, version, repos, primarykey)

    @classmethod
    def with_name(cls, repos, name, rev = None):
        """Return a Node for the package with the given name and revision, or None if none are found.

        If None is specified for the revision, the most recent revision of the package with this name
        is located."""
        if rev == None:
            version_str = " ORDER BY timestamp DESC"
        else:
            version_str = " AND VERSION = '%s'" % rev
        for row in repos.sql(("SELECT primarykey, name, version FROM tw_package WHERE name = '%s'" + version_str) % name):
            primarykey, name, version = row[0], row[1], row[2]
            return cls('/' + name, version, repos, primarykey)

    @classmethod
    def named_like(cls, repos, pattern):
        """Return a PackageNode for the most recent version of each package whose name
        matches 'pattern'."""
        for row in repos.sql("""SELECT DISTINCT ON (name) primarykey, name, version
                 FROM tw_package WHERE name LIKE '%s' ORDER BY name, timestamp DESC""" % pattern):
            primarykey, name, version = row[0], row[1], row[2]
            yield cls('/' + name, version, repos, primarykey)

    @classmethod
    def all(cls, repos):
        "Generate a collection of Nodes for the latest revisions of all known packages."
        for row in repos.sql("SELECT DISTINCT ON(name) primarykey, name, version FROM tw_package ORDER BY name, timestamp DESC"):
            primarykey, name, version = row[0], row[1], row[2]
            yield cls('/' + name, version, repos, primarykey)

class ClassNode(StoreNode):
    """A Class in the Store repository.

    Class nodes combine a variety of information about the class they model, such as the comment,
    structure, and class and instance methods and protocols.  All of these are rendered in a consistent
    manner by the get_contents method."""

    def __init__(self, path, rev, repos, id,
                 definition_id, comment_id, environment, superclass,
                 owning_package):
        StoreNode.__init__(self, path, rev, Node.FILE, repos)
        self.id = id
        self.definition_id, self.comment_id = definition_id, comment_id
        self.environment, self.superclass = environment, superclass

        self.owning_package = owning_package

    def get_contents(self):
        "Generator method over the Class's formatted contents."
        stream = cStringIO.StringIO()
        stream.write("{{{\n")

        # First: the class definition.
        stream.write(self.get_definition() + "\n\n")

        # Second: instance-side protocols and contained methods.
        for protocol in sorted(self.get_instance_protocols()):
            stream.write(str(protocol) + "\n\n")
            
            for method in protocol.methods:
                stream.write(method.source.strip() + "\n\n")

        # Third: class-side protocols and contained methods.
        # TODO
        
        stream.write("}}}\n")

        return stream

    def get_definition(self):
        "Get the definition string that creates this Class."
        for row in self.repos.sql("SELECT blobdata FROM tw_blob WHERE primarykey = %i" % self.definition_id):
            return _strac_decode(row[0])

    def get_comment(self):
        "Get the class comment string for this class, if any."
        if self.comment_id == 0:
            return ""
        for row in self.repos.sql("SELECT blobdata FROM tw_blob WHERE primarykey = %i" % self.comment_id):
            return _strac_decode(row[0])

    def get_instance_protocols(self):
        """Find all instance-side methods within this package.  Generate them grouped by
        protocol."""
        protocols = {}

        for row in self.repos.sql("""
              SELECT name, sourcecodeid, protocolname FROM tw_methodsview
              WHERE packageref = %i AND classname = '%s' """ % (self.owning_package.id, self.name)):
            method_name, source_id, protocol_name = row[0], row[1], row[2]
            if protocol_name not in protocols:
                protocols[protocol_name] = Protocol(protocol_name)
            
            source = None
            for row in self.repos.sql("SELECT blobdata FROM tw_blob WHERE primarykey = %i" % source_id):
                source = _strac_decode(row[0])
            if source == None:
                raise TracError('Unable to locate method source code.')
            method = Method(method_name, source)

            protocols[protocol_name].methods.append(method)

        return protocols.values()

    @classmethod
    def with_id(cls, repos, id, owning_package):
        """Create a ClassNode directly from a primary key.

        The class revision is indicated by the revision of the owning package."""
        for row in repos.sql("""
              SELECT name, definitionid, commentid, environmentstring, superclass
              FROM tw_classrecord
              WHERE primarykey = %i""" % id):
            name, definition_id, comment_id = row[0], row[1], row[2]
            environment, superclass = row[3], row[4]
            return cls(environment + '.' + name, owning_package.rev, 
                       repos, id, definition_id, comment_id,
                       environment, superclass, owning_package)

class Protocol:
    "Protocol is a light wrapper around a collection of methods."

    before = ['initialize-release', 'initial']
    after = ['private', 'pvt']

    def __init__(self, name):
        self.name = name
        self.methods = []

        self._is_before = any(self.name.find(pattern) != -1 for pattern in self.before)
        self._is_after = any(self.name.find(pattern) != -1 for pattern in self.after)

    def __str__(self):
        return '{' + self.name + '}'

    def __cmp__(self, other):
        if self._is_before:
            if other._is_before:
                return _str_cmp(self.name, other.name)
            return -1
        elif self._is_after:
            if other._is_after:
                return _str_cmp(self.name, other.name)
            return 1
        else:
            if other._is_before: return 1
            if other._is_after: return -1
            return _str_cmp(self.name, other.name)

class Method:
    "Method is a light wrapper to temporarily store data."

    def __init__(self, name, source):
        self.name = name
        self.source = source

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name == other.name:
            return 0
        else:
            return 1
