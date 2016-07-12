from twisted.python.components import registerAdapter
from nevow.athena import LiveElement
from xmantissa.webtheme import ThemedDocumentFactory
from xmantissa.ixmantissa import INavigableFragment, ITemplateNameResolver

class PonyCreatorView(LiveElement):
    """
    Web view for Pony management.
    """
    implements(INavigableFragment)

    title = u'Pony management'
    docFactory = ThemedDocumentFactory('pony-creator', 'resolver')

    def __init__(self, ponyCreator):
        super(PonyCreatorView, self).__init__()
        self.ponyCreator = ponyCreator
        self.resolver = ITemplateNameResolver(self.ponyCreator.store.parent)

registerAdapter(PonyCreatorView, PonyCreator, INavigableFragment)
