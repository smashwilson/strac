# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from storenode import StoreNode
from packagenode import PackageNode

class BundleNode(StoreNode):
    """A Bundle in the Store repository.

    Data about bundles is stored in the tw_bundle table.
    """

    def __init__(self, path, rev, repos, id):
        StoreNode.__init__(self, path, rev, StoreNode.DIRECTORY, repos)
        self.id = id

    def get_entries(self):
        """Generator method that produces the PackageNodes and BundleNodes contained in this bundle."""
        
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
