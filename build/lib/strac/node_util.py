"""
Utility classes and methods.
"""

from base64 import b64decode

def _strac_decode(blob):
    """Decode Store textual data from the table tw_blob into a Python string."""

    return b64decode(blob).replace("\r", "\n")

def _str_cmp(a, b):
    """Because it looks like Python doesn't have one (?)"""

    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1

class Protocol:
    """A protocol is a method category within a Smalltalk class.

    Protocols are used to coallate data about methods between the SQL that retrieves them
    and the creation of a hierarchy of ClassNodes to represent them.  Protocols also serve
    to order themselves in the traditional Smalltalk ordering: initialization, others in
    alphabetical order, then private protocols, all in alphanumeric order within their
    categories.
    """

    before = ['initialize-release', 'initial']
    after = ['private', 'pvt']

    def __init__(self, name):
        self.name = name
        self.methods = []

        self._is_before = any(self.name.find(pattern) != -1 for pattern in self.before)
        self._is_after = any(self.name.find(pattern) != -1 for pattern in self.after)

    def add_method(self, method):
        self.methods.append(method)

    def get_methods(self):
        return self.methods

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
    """Method is a light wrapper to organize source code.
    """

    def __init__(self, name):
        self.name = name
        self.source = None

    def set_source(self, source):
        self.source = source

    def get_source(self):
        return self.source

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name == other.name:
            return 0
        else:
            return 1

class SharedVariable:
    """Classes and Namespaces may define one or more shared-scope variables.

    Shared variables are presented as definitions within the content of their
    environments.
    """

    def __init__(self, name):
        self.name = name
        self.definition = ''

    def set_definition(self, definition):
        self.definition = definition

    def get_definition(self):
        return self.definition

    def __cmp__(self, other):
        if self.name < other.name:
            return -1
        elif self.name == other.name:
            return 0
        else:
            return 1
