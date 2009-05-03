# Implements the interfaces required for a Trac version control plugin, as specified
# in trac/versioncontrol/api.py.

from time import time

from trac.core import Component, TracError, implements

from trac.config import Option

from trac.versioncontrol.api import IRepositoryConnector, Repository, Node
from trac.versioncontrol.api import Changeset, Authorizer
from trac.versioncontrol.api import NoSuchChangeset, NoSuchNode, PermissionDenied

from strac.nodes import RootNode, BundleNode, PackageNode

try:
    import pgdb
except ImportError:
    has_pgdb = False
else:
    has_pgdb = True

class StoreConnector(Component):
    "Component that registers the Store repository type with the Trac repository manager."

    root_store_bundle = Option('trac', 'root_store_bundle', '',
       """Use this bundle as the root of the Store repository view.""")

    root_store_package = Option('trac', 'root_store_package', '',
       """Use the collection of packages that begin with this string as the
          root of the Store repository view.""")

    implements(IRepositoryConnector)

    def get_supported_types(self):
        "Generate tuples of (name, priority)."
        global has_pgdb
        if has_pgdb:
            yield ('store', 4)

    def get_repository(self, repos_type, repos_name, authname):
        "Return an instance of a Store repository."
        root_store_bundle = self.config['trac'].get('root_store_bundle')
        root_store_package = self.config['trac'].get('root_store_package')

        return StoreRepository(repos_name, root_store_bundle, root_store_package, authname, self.log)

class StoreRepository(Repository):
    "Mediates communications with the Store repository in a database."

    def __init__(self, repos_name, root_store_bundle, root_store_package, authz, log):
        """Initialize the repository.

        This call creates the database connection.  repos_name is expected to be a valid database
        connection string.  One of root_store_bundle and root_store_package must specify what to
        consider as the root of the Store repository view: if neither are provided, the full repository
        will be visible.
        """
        Repository.__init__(self, repos_name, authz, log)

        self.connection = pgdb.connect(repos_name)    
        self.root = RootNode(self, root_store_bundle, root_store_package)

    def close(self):
        self.connection.close()

    def clear(self, youngest_rev = None):
        pass

    def get_changeset(self, rev):
        # Stub
        return StoreChangeset(rev, 'Dummy changeset', 'smash', time())

    def has_node(self, path, rev = None):
        pass

    def get_node(self, path, rev = None):
        if not path or path == '/': return self.root
        parts = path.split('/')
        if parts[0] == '': parts = parts[1:]
        if len(parts) == 1:
            bundle = BundleNode.with_name(self, parts[0], rev)
            if bundle != None: return bundle
            package = PackageNode.with_name(self, parts[0], rev)
            if package != None: return package
            
            raise NoSuchNode(path, rev)
        else:
            package = PackageNode.with_name(self, parts[-2], rev)
            if package != None:
                fullclass = parts[-1]
                classname = fullclass.split('.')[-1]
                environment = fullclass[:-len(classname)-1]
                return package.class_named(environment, classname)

    def get_oldest_rev(self):
        # Stub
        return None

    def get_youngest_rev(self):
        # Stub
        return None

    def previous_rev(self, rev):
        pass

    def next_rev(self, rev, path = ''):
        pass

    def rev_older_than(self, rev1, rev2):
        pass

    def get_path_history(self, path, rev = None, limit = None):
        pass

    def normalize_path(self, path):
        """Construct a canonical representation of a Store path.

        A canonical Store path is very simple: it is either the root (/),
        a bundle (/name), a package (/name), or a class in a package (/package/class).
        Any other extensions are reducible to this by the simple mechanism of cutting
        off any prefixing bits."""
        if path == '/': return path
        parts = path.split('/')
        if parts[0] == '':
            parts[0:1] = []
        last = parts[-1]
        if PackageNode.with_name(self, last) != None or BundleNode.with_name(self, last) != None:
            return '/' + last
        else:
            return '/' + '/'.join(parts[-2:])

    def normalize_rev(self, rev):
        pass

    def get_changes(self, old_path, old_rev, new_path, new_rev, ignore_ancestry = 1):
        pass

    def sql(self, string):
       "Generator over the results of executing the SQL 'string'."
       cursor = self.connection.cursor()
       try:
           cursor.execute(string)
           for i in range(cursor.rowcount):
               yield cursor.fetchone()
       finally:
           cursor.close()

class StoreChangeset(Changeset):
    "A single 'publishing' of a package."

    def __init__(self, rev, message, author, date):
        Changeset.__init__(self, rev, message, author, date)

    def get_changes(self):
        pass
