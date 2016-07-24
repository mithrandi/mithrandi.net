.. title: WordPress to Nikola
.. slug: wordpress-to-nikola
.. date: 2016-07-24 17:35:33 UTC
.. tags: blog, wordpress, nikola
.. category: 
.. link: 
.. description: 
.. type: text

As you may or may not have noticed, my blog looks substantially different now.
This is because I have migrated from `WordPress`_ to `Nikola`_. Using the
WordPress importer worked out reasonably well, although I needed to fix up the
code blocks myself. Going forward I'm just going to use the standard ReST
format for writing posts.

.. _WordPress: https://wordpress.org/
.. _Nikola: https://getnikola.com/

I'm also hosting the site on S3 with CloudFront in front, rather than a dinky
Linode, so the site should be a lot faster now. However, there's probably some
stuff broken that I didn't notice; please yell if you see anything.
