# Copyright (C) 2009 Ashley J. Wilson
# This software is licensed as described in the file COPYING in the root
# directory of this distribution.

from storenode import StoreNode
from bundlenode import BundleNode
from packagenode import PackageNode

class RootNode(StoreNode):
    """The virtual root of a Store repository.

    This node has as its children the BundleNode and/or set of PackageNodes,
    that are specified by the trac.ini file as the interesting part of
    the Store repository.  RootNodes have only the special revision 'ONLY' and
    no previous or next changeset.
    """

    def __init__(self, repos, bundle_desc, package_desc):
        """Create a RootNode that will report the interesting subset of the Store
        repository as its children.

        bundle_desc is expected to be either an exact bundle name from Store, or a
        comma-separated list of the same.  Similarly, package_desc is either one or
        many package prefixes.  Either parameter may be 'ALL', which will return every
        such entity in the repository, or '', which will return nothing of that type.
        """

        StoreNode.__init__(self, '/', 'ONLY', StoreNode.DIRECTORY, repos)

        if not bundle_desc:
            self.bundle_names = []
        else:
            self.bundle_names = [bn.strip() for bn in bundle_desc.split(',')]

        if not package_desc:
            self.package_prefixes = []
        else:
            self.package_prefixes = [pp.strip() for pp in package_desc.split(',')]

    def get_entries(self):
        """Generator method for the PackageNodes and/or BundleNodes contained
        within this view of the repository.
        """

        for bundle_name in self.bundle_names:
            if bundle_name == 'ALL':
                for bnode in BundleNode.all(self.repos):
                    yield bnode
            elif bundle_name != None:
                yield BundleNode.with_name(self.repos, bundle_name)
        
        for package_prefix in self.package_prefixes:
            if package_prefix == 'ALL':
                for pkg in PackageNode.all(self.repos):
                    yield pkg
            elif package_prefix != None:
                for pkg in PackageNode.named_like(self.repos, package_prefix + '%'):
                    yield pkg
