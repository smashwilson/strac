from test.strac_test import StoreTestCase

from strac.repos import StoreRepository, StoreConnector, StoreChangeset
from strac.bundlenode import BundleNode
from strac.classnode import ClassNode

from time import time

class TestRepository(StoreTestCase):

    def test_connector(self):
        """Make sure that the Store connector properly loads the database modules."""

        self.assertTrue(('store', 4) in self.conn.get_supported_types())

    def test_connect_to_database(self):
        """Make sure that the connector connects to something."""

        self.assertTrue(self.repos != None)

    def test_root_access(self):
        """Pull configuration options from trac.ini and ensure that the root node behaves
        accordingly.
        """

        self.assertEquals('TestBundle', self.env.config['trac'].get('root_store_bundles'))

        self.node = self.repos.get_node('/')
        self.assertTrue(self.node != None)
    
        contents = self.node.get_entries()
        self.assertEquals('TestBundle', contents.next().get_name())

    def test_normalize_path(self):
        """Stress test path normalization for a variety of cases."""

        for path in ['/', '/TestBundle', '/TestPackage2']:
            self.assertEquals(path, self.repos.normalize_path(path))

        self.assertEquals(
            '/TestPackage2/StracTest.StracClass11',
            self.repos.normalize_path('/TestPackage2/Root.Smalltalk.StracTest.StracClass11'))

        self.assertEquals(
            '/TestPackage2',
            self.repos.normalize_path('/TestBundle/TestPackage2'))

        self.assertEquals(
            '/TestPackage2/StracTest.StracClass11',
            self.repos.normalize_path('/TestBundle/TestPackage2/StracTest.StracClass11'))

        self.assertEquals('/', self.repos.normalize_path(None))

    def test_get_node(self):
        """Test the get_node() method for bundles, packages, and classes."""

        node0 = self.repos.get_node('/TestBundle')

        self.assertEquals('TestBundle', node0.name)
        self.assertEquals(3, len([n for n in node0.get_entries()]))

        node1 = self.repos.get_node('/TestPackage2')

        self.assertEquals(3, len([n for n in node1.get_entries()]))

        node2 = self.repos.get_node('/TestPackage2/StracTest.StracClass21')

        self.assertEquals(ClassNode, node2.__class__)

    def test_revision_stubs(self):
        """Assert that the calls relating for revisions are properly stubbed, that is,
        they don't toss exceptions in normal usage.
        """

        # Called during a timeline view
        events = [e for e in self.repos.get_changesets(time(), time())]

        # Called during changeset view
        self.repos.authz.assert_permission_for_changeset('ONLY')
        self.repos.get_node('/').get_previous()
        [chg for chg in StoreChangeset('ONLY', 'Test', 'test', time()).get_changes()]

        # Called during revision log view
        [(p, r, h) for (p, r, h) in self.repos.get_node('/TestPackage1', 'None').get_history()]
        [(p, r, h) for (p, r, h) in self.repos.get_path_history('/', None, None)]

        # Called during 'get changes' session
        [(o, n, k, c) for (o, n, k, c) in self.repos.get_changes('/TestPackage1', '1.0', '/TestPackage1', '1.1')]

        self.assertTrue(True, 'get_changesets() returned an iterable')
