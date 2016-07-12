from twisted.python.filepath import FilePath

from xmantissa.offering import Offering

import ponies
from ponies.ponies import PonyCreator
from ponies.rainbows import RainbowEditor
from ponies.theme import PoniesTheme

plugin = Offering(
    name=u'Ponies',
    description=u"""
    A web-based system for generating ponies.
    """,
    siteRequirements=[],
    appPowerups=[],
    installablePowerups=[(u'ponies', u'Pony creation and editing', PonyCreator),
                         (u'rainbows', u'Rainbow editing', RainbowEditor)],
    loginInterfaces=[],
    themes=[PoniesTheme('base', 0)],
    version=ponies.version,
    staticContentPath=FilePath(ponies.__file__).sibling('static'))
