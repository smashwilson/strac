from trac.versioncontrol.api import Node

import repos

class StoreNode(Node):
    """A single node in a Store repository virtual tree.

    In Store, a node can be either a virtual root node, a bundle, a package, or a class.
    """

    def __init__(self, path, rev, kind, repos):
        Node.__init__(self, path, rev, kind)
        self.repos = repos

    def get_content(self):
        return None

    def get_entries(self):
        return None

    def get_history(self, limit = None):
        # Temporary stub for 'previous revision'
        self.repos.log.debug('path = <%s> rev = <%s>' % (self.path, self.rev))
        return [(self.path, self.rev, repos.StoreChangeset.EDIT)]

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

    def _normalize_name(self, name):
        """Remove any Root.Smalltalk. prefix from the fully-qualified class or namespace name."""

        if name.startswith('Root.Smalltalk.'):
            return name[len('Root.Smalltalk.'):]
        else:
            return name

    def _write_protocols(self, stream, header, protocols):
        """Format methods and protocols properly to stream, in good wiki format.

        If protocols is nonempty, prefix it with header.
        """

        if len(protocols) != 0:
            stream.write(header)
            stream.write("\n")

        for protocol in sorted(protocols):
            stream.write("\n''")
            stream.write(str(protocol))
            stream.write("''\n\n")
            
            for method in sorted(protocol.get_methods()):
                stream.write("{{{\n")
                stream.write(method.source.strip())
                stream.write("\n}}}\n")

    def _write_comment(self, stream, header, comment_text):
        """Format a class or namespace comment properly to stream, in good wiki format.

        If comment is nonempty, prefix it with header.
        """

        if comment_text != '':
            stream.write(header)
            stream.write("\n\n")
            stream.write(comment_text.strip())
            stream.write("\n\n")

    def _write_shared_vars(self, stream, header, shared_vars):
        """Display the definition of each shared variable in shared_vars.

        The shared_vars is nonempty, prefix it with header.
        """

        if len(shared_vars) != 0:
            stream.write(header)
            stream.write("\n\n")

        for shared_var in sorted(shared_vars):
            stream.write("{{{\n")
            stream.write(shared_var.get_definition())
            stream.write("\n}}}\n")
