.. title: Progress on txacme
.. slug: progress-on-txacme
.. date: 2016-08-15 17:40:28 UTC
.. tags: python,tech,txacme,letsencrypt
.. category: 
.. link: 
.. description: 
.. type: text

The initial release of `txacme`_ was perhaps a quieter affair than I was hoping
for, but the response has been enthusiastic from the few people that did take
notice. Work has been progressing on the next release (which will be 0.9.1, I'm
not at all ready to pronounce the API fully baked yet), which will have a
number of minor improvements such as better documentation, but the headline
feature is probably ``dns-01`` challenge support.

.. _txacme: https://github.com/mithrandi/txacme

There is currently a `PR`_ up with a `libcloud`_\-based implementation that
works [#]_; I also have plans for a `twistd plugin`_ to run a standalone
issuing service, but I'm not yet sure if this will make it into `0.9.1`_.

.. _PR: https://github.com/mithrandi/txacme/issues/59
.. _libcloud: https://libcloud.apache.org/
.. _twistd plugin: https://github.com/mithrandi/txacme/issues/62
.. _0.9.1: https://github.com/mithrandi/txacme/milestone/2

Implementing a ``dns-01`` challenge responder revealed some deficiencies in the
``IResponder`` interface that made it necessary to expand it; this is exactly
the sort of API change that I was expecting to crop up, and one of the reasons
why I'm holding off on a 1.0.0 release for the time being. My guess is that
I'll make it to at least 0.9.5 or thereabouts before 1.0.0 comes out.

.. rubric:: Footnotes

.. [#] Well... mostly. libcloud does synchronous network I/O so it needs to be
       invoked in a thread pool, and some of the DNS drivers are buggy (eg. the
       Route 53 driver does not format TXT records how Route 53 expects them),
       but I have a passing integration test using Rackspace Cloud DNS!
