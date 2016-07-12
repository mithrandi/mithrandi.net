from zope.interface import implements
from axiom.item import Item
from axiom.attributes import integer
from xmantissa.ixmantissa import INavigableElement
from xmantissa.webnav import Tab


class PonyCreator(Item):
    """
    Powerup for creating and managing ponies.
    """
    implements(INavigableElement)
    powerupInterfaces = [INavigableElement]

    ponyQuota = integer(allowNone=False, default=10)

    def getTabs(self):
        return [Tab('ZOMG PONIES!', self.storeID, 1.0)]
