from plone.resource.traversal import ResourceTraverser


class SantaPerpetuaTraverser(ResourceTraverser):
    """The vilaix theme santa perpetua traverser.

    Allows traversal to /++VilaixTheme++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'santaperpetua'
