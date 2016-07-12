This is the fourth post in a `series of articles`_ about `Mantissa`_.

.. _series of articles: link://tag/mantissa-intro
.. _Mantissa: https://github.com/twisted/mantissa

In `the previous article`_ I described how an offering can provide powerups to
be included in a product, which will then be installed on a user store; in this
installment, I will discuss what form these powerups can actually take, and how
they allow you to expose your application's functionality to the user.

.. _the previous article: https://mithrandi.net/blog/2010/07/an-introduction-to-mantissa-part-2-offerings/

One of the most commonly-implemented powerup interfaces in Mantissa is
``INavigableElement``. Mantissa has a somewhat generalized idea of
"navigation", whereby a nested menu structure can be defined through
``INavigableElement`` powerups, and then displayed by different implementations
for different protocols; for example, the web view has a visual dropdown menu
system, whereas the SSH server presents a textual menu system. A typical
``INavigableElement`` powerup implementation will look something like this:

.. listing:: pony_navigable.py python

``INavigableElement`` only has one method, ``getTabs``, which returns a list of
"tabs" or menu items to be presented in the nav. The primary components of a
tab are a title (which is how the item is displayed in the UI), the ``storeID``
of an item in the same store which the tab points to, and a float between 0.0
and 1.0 indicating the sort priority of the tab (higher values sort sooner). In
this case, we have the tab pointing directly at the ``PonyCreator`` item
itself; in order for this to work, we'll need some extra code to allow
``PonyCreator`` to be exposed via the web.

In order for an item in a user's store to be privately accessible via the web
by that user, it needs to be adaptable to the (somewhat poorly-named)
``INavigableFragment`` interface. This is almost always done by defining an
adapter from the item type to ``INavigableFragment``:

.. listing:: pony_view.py python

Our element will be wrapped in the Mantissa shell when it is rendered, so we
cannot control the page title directly from the template, but the title
attribute provides a way for our element to specify the page title.
``ThemedDocumentFactory`` is used to retrieve the template through the theme
system; the arguments are the name of the template (``'pony-creator'``) and the
name of the attribute holding the ``ITemplateNameResolver`` implementation used
to retrieve the template. This attribute is set in ``__init__`` using a
slightly awkward method; the template resolver should really be passed in by
Mantissa somehow, but currently there is no mechanism for doing this, so
instead we retrieve the default resolver ourselves from the site store.

This is all that is needed for hooking some code up to the web view; any
further UI behaviour would be implemented in HTML / JavaScript in
``PonyCreatorView``, usually by invoking additional methods defined on
``PonyCreator``.

Next up: Sharing, or "How do I publish public / shared content?"
