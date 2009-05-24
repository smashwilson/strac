# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.
#
# Implements the interfaces required for a Trac version control plugin, as
# specified in trac/versioncontrol/api.py.

from datetime import datetime
from trac.util.datefmt import utc

from trac.core import Component, TracError, implements

from trac.config import Option

from trac.versioncontrol.api import IRepositoryConnector, Repository, Node
from trac.versioncontrol.api import Changeset, Authorizer
from trac.versioncontrol.api import NoSuchChangeset, NoSuchNode, PermissionDenied

from rootnode import RootNode
from bundlenode import BundleNode
from packagenode import PackageNode

try:
    import pgdb
except ImportError:
    has_pgdb = False
else:
    has_pgdb = True

class StoreConnector(Component):
    """
    Component that registers the Store repository type with the Trac
    repository manager.
    """

    store_database_connection = Option('strac', 'store_database_connection',
        '',
        """
        Database connection string that points to your Store repository.  See
        your database's documenation for the format to use.
        """)

    root_store_bundle = Option('strac', 'root_store_bundles', '',
        """
        Use this bundle as the root of the Store repository view.  You may
        specify several bundles as a comma-separated list, or the special
        value ALL to include all bundles.
        """)

    root_store_package = Option('strac', 'root_store_packages', '',
       """
       Use the collection of packages that begin with this string as the root
       of the Store repository view.  You may specify several prefixes as a
       comma-separated list, or the special value ALL to include all packages.
       """)

    implements(IRepositoryConnector)

    # IRepositoryConnector required methods.

    def get_supported_types(self):
        """Generate tuples of (name, priority)."""

        global has_pgdb
        if has_pgdb:
            yield ('store', 4)

    def get_repository(self, repos_type, repos_name, authname):
        """Return an instance of a Store repository."""

        connection_string = self.config['strac'].get('store_database_connection')
        root_store_bundles = self.config['strac'].get('root_store_bundles')
        root_store_packages = self.config['strac'].get('root_store_packages')
        return StoreRepository(connection_string, root_store_bundles,
                               root_store_packages, None, self.log)

class StoreRepository(Repository):
    """Mediates communications with the Store repository in a database."""

    def __init__(self, connection_string, root_store_bundle, root_store_package, authz, log):
        """Initialize the repository.

        This call creates the database connection.  repos_name is expected to be a valid database
        connection string.  One of root_store_bundle and root_store_package must specify what to
        consider as the root of the Store repository view: if neither are provided, the full repository
        will be visible.
        """
        Repository.__init__(self, connection_string, authz, log)
        self.connection = pgdb.connect(connection_string)
        self.root = RootNode(self, root_store_bundle, root_store_package)

    def close(self):
        self.connection.close()

    def clear(self, youngest_rev = None):
        pass

    def get_changeset(self, rev):
        # Temporary stub
        return StoreChangeset.working_on_it()

    def get_changesets(self, start, stop):
        # Temporary stub (needed so that the Timeline component won't break horribly)
        return []

    def get_node(self, path, rev = None):
        """Return a StoreNode subclass appropriate to handle the resource at path and rev."""

        # Case 1: Root
        if not path or path == '/': return self.root

        parts = path.split('/')
        if parts[0] == '': parts = parts[1:]

        # Workaround to deal with us wanting to use None revisions
        # in places where unicode() is used
        if rev == 'None': rev = None

        if len(parts) == 1:
            # Case 2: /BundleName
            bundle = BundleNode.with_name(self, parts[0], rev)
            if bundle != None: return bundle

            # Case 3: /PackageName
            package = PackageNode.with_name(self, parts[0], rev)
            if package != None: return package            
        else:
            # Case 4: /PackagName/Fully.Qualified.ClassName
            package = PackageNode.with_name(self, parts[-2], rev)
            if package != None:
                subnode = package.subnode_named(parts[-1])
                if subnode != None: return subnode
        raise NoSuchNode(path, rev)

    def get_oldest_rev(self):
        # Temporary stub.
        return None

    def get_youngest_rev(self):
        # Temporary stub.
        return None

    def previous_rev(self, rev):
        pass

    def next_rev(self, rev, path = ''):
        pass

    def rev_older_than(self, rev1, rev2):
        pass

    def get_path_history(self, path, rev = None, limit = None):
        # Temporary stub
        return [(path, rev, StoreChangeset.EDIT)]

    def normalize_path(self, path):
        """Construct a canonical representation of a Store path.

        A canonical Store path is very simple: it is either the root (/),
        a bundle (/name), a package (/name), or a class in a package (/package/class).
        Any other extensions are reducible to this by the simple mechanism of cutting
        off any prefixing bits.
        """

        if path == None or path == '/':
            # Root
            return '/'

        parts = path.split('/')
        if parts[0] == '':
            parts[0:1] = []
        last = parts[-1]

        if PackageNode.with_name(self, last) != None or PackageNode.with_name(self, last) != None:
            # Bundle/Package or Bundle/Bundle ... all but the last element are unnecessary.
            return '/' + last
        else:
            # Package/Class ... normalize Class by stripping any Root.Smalltalk prefix.
            if last.startswith('Root.Smalltalk.'):
                last = last[len('Root.Smalltalk.'):]
            if len(parts) >= 2:
                return '/' + parts[-2] + '/' + last
            else:
                return '/' + last

    def normalize_rev(self, rev):
        return rev

    def get_changes(self, old_path, old_rev, new_path, new_rev, ignore_ancestry = 1):
        # Temporary stub
        old = self.get_node(old_path, old_rev)
        new = self.get_node(new_path, new_rev)
        return [(old, new, StoreChangeset.EDIT, StoreChangeset.working_on_it(new_rev))]

    def sql(self, string):
       """Generator over the results of executing the SQL 'string'."""

       cursor = self.connection.cursor()
       try:
           cursor.execute(string)
           for i in range(cursor.rowcount):
               yield cursor.fetchone()
       finally:
           cursor.close()

class StoreChangeset(Changeset):
    """One 'publishing' of a package to Store.

    Contains information such as blessings and comments.
    """

    def get_changes(self):
        # Temporary stub.
        return []

    def get_properties(self):
        # Temporary stub.
        return {}

    @classmethod
    def working_on_it(cls, rev = None):
        return cls(rev, 
                   "Changeset support is not yet implemented in Strac.  I'm working on it!",
                   'smash',
                   datetime.now(utc))
