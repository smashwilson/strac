# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from storenode import StoreNode
from classnode import ClassNode
from classextensionnode import ClassExtensionNode
from namespacenode import NamespaceNode

from node_util import _strac_decode, Method, Protocol, SharedVariable

class PackageNode(StoreNode):
    """A Package in the Store repository.

    Data about packages is stored in the tw_package table."""

    def __init__(self, path, rev, repos, id):
        StoreNode.__init__(self, path, rev, StoreNode.DIRECTORY, repos)
        self.id = id

    def get_entries(self):
        """Generator method that produces the subnodes contained in this package.

        Note that subnodes are constructed with the minimum possible database work: class definitions
        and method sources are not available for each entry.  To access a subnode for in-depth work,
        use subnode_named().
        """

        # Start by finding the namespaces within this package.
        for row in self.repos.sql("SELECT name, environmentstring FROM tw_pkgnamespacesview WHERE packageref = %i" % self.id):
            fullname = row[1] + '.' + row[0]
            yield NamespaceNode.just_named(fullname, self)

        # Find the names of all classes that have methods defined by this package.  Filter out the metaclasses.
        classes_touched = []
        for row in self.repos.sql("SELECT DISTINCT classname FROM tw_methodsview WHERE packageref = %i" % self.id):
            classname = row[0]
            if classname.endswith(' class'):
                classname = classname[:-6]
            classes_touched.append(classname)
        classes_touched = set(classes_touched)

        # Find classes defined within this package.  Yield a ClassNode for each and remember the yielded class
        # names.
        classes_defined = []
        for row in self.repos.sql("SELECT name, environmentstring FROM tw_pkgclassesview WHERE packageref = %i" % self.id):
            fullname = row[1] + '.' + row[0]
            classes_defined.append(fullname)
            yield ClassNode.just_named(fullname, self)

        # Yield a ClassExtensionNode for each class name that didn't have a definition in this package.
        for extended_class_name in [c for c in classes_touched if c not in classes_defined]:
            yield ClassExtensionNode.just_named(extended_class_name, self)

    def subnode_named(self, fullname):
        """Return a fully-initialized ClassNode, ClassExtensionNode, or NamespaceNode within this package
        and uniquely identified by a fully-qualified 'fullname'.
        """
        # Prefix the fullname with a Root.Smalltalk. if it isn't there already.
        if not fullname.startswith('Root.Smalltalk.'):
            fullname = 'Root.Smalltalk.' + fullname

        parts = fullname.split('.')
        environment, class_name = '.'.join(parts[:-1]), parts[-1]

        # Collect any shared variables declared in this environment (class or namespace).
        svars = []
        for row in self.repos.sql("""
              SELECT name, blobdata FROM tw_dataandsourcesview
              WHERE packageref = %i AND environmentstring = '%s'
              """ % (self.id, fullname)):
            name, definition = row[0], _strac_decode(row[1])
            svar = SharedVariable(name)
            svar.set_definition(definition)
            svars.append(svar)

        # Look for a Namespace with this name first.
        for row in self.repos.sql("""
              SELECT primarykey, commentid, blobdata FROM tw_pkgnamespacesandsourcesview
              WHERE packageref = %i AND name = '%s' AND environmentstring = '%s'
              """ % (self.id, class_name, environment)):
            namespace_id, comment_id, definition = row[0], row[1], _strac_decode(row[2])
            return NamespaceNode.fully_initialized(fullname, namespace_id, self,
                                                   definition, comment_id, svars)

        # Collect instance- and class-side Methods defined for this class, within this package.
        # Organize them into Protocols.
        iprotocols = self._get_protocols_for(fullname)
        cprotocols = self._get_protocols_for(fullname + ' class')
        

        # Look for the class definition in tw_pkgclassesview.  If it's there, return the subnode
        # as a ClassNode.
        for row in self.repos.sql("""
              SELECT primarykey, commentid, blobdata FROM tw_pkgclassesandsourcesview
              WHERE packageref = %i AND name = '%s' AND environmentstring = '%s'
              """ % (self.id, class_name, environment)):
            primarykey, comment_id, definition = row[0], row[1], _strac_decode(row[2])
            return ClassNode.fully_initialized(fullname, primarykey, self,
                                               definition, comment_id,
                                               iprotocols, cprotocols, svars)

        # If it isn't there, but we found some methods defined for this class,
        # return a ClassExtensionNode.
        if len(iprotocols) != 0 or len(cprotocols) != 0:
            return ClassExtensionNode.fully_initialized(fullname, self,
                                                        iprotocols, cprotocols, svars)

        # No methods or definitions found: return None.
        return None

    def _get_protocols_for(self, class_name):
        """Private method used by subnode_named() to fetch all methods defined within this
        package for a class called class_name, organized in a structure of Protocols.
        """

        protocols = {}
        methods_by_source_id = {}
        for row in self.repos.sql("""
              SELECT primarykey, name, sourcecodeid, protocolname FROM tw_methodsview
              WHERE packageref = %i AND classname = '%s'
              """ % (self.id, class_name)):
            method_id, method_name, source_id, protocol_name = row[0], row[1], row[2], row[3]
            if protocol_name not in protocols:
                protocols[protocol_name] = Protocol(protocol_name)

            protocol = protocols[protocol_name]
            method = Method(method_name)

            protocol.add_method(method)
            methods_by_source_id[source_id] = method

        # Fetch the source code for all of these methods in a single query.
        if len(methods_by_source_id) != 0:
            id_str = ', '.join(str(id) for id in methods_by_source_id.keys())
            for row in self.repos.sql("""
                  SELECT primarykey, blobdata FROM tw_blob WHERE primarykey IN (%s)
                  """ % id_str):
                primarykey, source = row[0], _strac_decode(row[1])
                methods_by_source_id[primarykey].set_source(source)

        return protocols.values()

    @classmethod
    def with_id(cls, repos, id):
        """Fetch a PackageNode directly by its primary key."""

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
        matches 'pattern'.
        """

        for row in repos.sql("""
                 SELECT DISTINCT ON (name) primarykey, name, version
                 FROM tw_package WHERE name LIKE '%s'
                 ORDER BY name, timestamp DESC""" % pattern):
            primarykey, name, version = row[0], row[1], row[2]
            yield cls('/' + name, version, repos, primarykey)

    @classmethod
    def all(cls, repos):
        """Generate a collection of Nodes for the latest revisions of all known packages."""

        for row in repos.sql("SELECT DISTINCT ON(name) primarykey, name, version FROM tw_package ORDER BY name, timestamp DESC"):
            primarykey, name, version = row[0], row[1], row[2]
            yield cls('/' + name, version, repos, primarykey)
