This is the third post in a `series of articles`_ about `Mantissa`_.

.. _series of articles: link://tag/mantissa-intro
.. _Mantissa: https://github.com/twisted/mantissa

The primary code entry point in Mantissa is the offering. Your application can
provide an ``IOffering`` plugin in ``xmantissa.plugins``, which hands some
chunks of your code over to be used by Mantissa. There is no real reason to
implement ``IOffering`` yourself; instead, simply instantiate
``xmantissa.offering.Offering`` in your plugin module. For example, you might
have an ``xmantissa/plugins/ponies.py`` module containing the following code:

.. listing:: ponies.py python

There are a number of elements here, some of which we will only return to
later, but I'll run through all of them here briefly.

* name: A short identifier used as the name of this offering.
* description: A long description explaining what this offering is.
* siteRequirements: Interfaces that this offering requires from the site store.
* appPowerups: Powerups to be installed on the app store.</li>
* installablePowerups: A list of 3-tuples, ``(name, description, item class)``.
  Each of these tuples describes a powerup that can potentially be installed on
  a user store.
* loginInterfaces: This allows your offering to provide additional ways of
  logging into Mantissa. For example, a webmail offering might provide
  interfaces that are used when logging in via SMTP or POP3.
* themes: The themes system provides a way to provide and override the
  templates used by your widgets.
* staticContentPath: A path pointing at the root of your static content. The
  file hierarchy at this location will be served up by Mantissa at
  ``/static/YourOfferingName``.
* version: A ``Version`` object specifying the version number of your offering.

For more information, take a look at ``xmantissa.ixmantissa.IOffering``, which
documents each of these attributes in more detail. The main highlights here,
though, are ``appPowerups``, for the powerups you want installed on the app
store, and ``installablePowerups``, for powerups you want to be available for
installation on the user store.

To set up a Mantissa site, the first step is to run ``axiomatic mantissa``;
this will prompt you for an admin password as part of installing the base
Mantissa components. To start the site up, you run ``axiomatic start``; usually
you would pass the ``--nodaemon`` flag during development, which prevents the
server from daemonizing, and directs log output to the console instead of to a
log file. If you log in as the admin user (``admin@localhost`` by default) via
the web interface, you can install an Offering through the admin UI;
alternatively, you can install offerings from the command line by running
``axiomatic offering install SomeOfferingName``.

When your offering is installed, the powerups in ``appPowerups`` will be
installed onto the app store for your offering. The ``installablePowerups`` you
provided will not be installed anywhere immediately, instead they will be
exposed in the admin UI for products. A product is an administratively-defined
collection of powerups; the admin can select any of the ``installablePowerups``
from any of the installed offerings when creating a product. Products are used
in conjunction with signup methods, which are also locally configured by the
admin. A signup has a product associated with it; when a user signs up using
this method, all of the powerups that comprise the product will be installed on
their user store.

Whew! This may all seem like more indirection than is actually necessary, but
if you view Mantissa as a layer that multiplexes between users and
applications, it may make a little more sense.

Next up: Powerup interfaces, or "How does the user actually interact with my code?"
