[NOTE: If you are reading this post in an RSS reader, the formatting on the
code examples may not be optimal; please read this in a web browser with
JavaScript enabled for the optimal viewing experience]

Introduction
============

I often find myself helping newer Twisted users come to grips with arranging
their flow control when they first start writing code that uses Deferreds.
While the `Deferred Reference`_ does a reasonable job of covering all of the
details, it is often difficult to make the intuitive leap from the synchronous
patterns one is used to, to their asynchronous equivalents. To that end, I
often find that comparing sync and async versions is illustrative; there are
some examples of this nature in the Deferred Reference, but some patterns are
missing, and I've never actually put all of the examples down in one place, so
I thought I'd do that in my blog post. Without any further ado, here they are:

.. _Deferred Reference: http://twistedmatrix.com/documents/current/core/howto/defer.html

EDIT: Added composition example

Call a function, and use the result
-----------------------------------

.. code:: python 

   # Synchronous version
   result = getSomething()
   doSomething(result)

   # Asynchronous version
   d = getSomething()
   d.addCallback(doSomething)


Call a function and use the result, catching a particular exception
-------------------------------------------------------------------

.. code:: python   

   # Synchronous version
   try:
       result = getSomething()
       doSomething(result)
   except SomeException as e:
       handleError(e)

   # Asynchronous version
   def _eb(f):
       f.trap(SomeException)
       handleError(f)
       
   d = getSomething()
   d.addCallback(doSomething)
   d.addErrback(_eb)


Call a function and use the result, catching any exception
----------------------------------------------------------

.. code:: python

   # Synchronous version
   try:
       result = getSomething()
       doSomething(result)
   except:
       log.err()

   # Asynchronous version
   d = getSomething()
   d.addCallback(doSomething)
   d.addErrback(log.err)


Call a function and use the result, catching exceptions raised by that function
-------------------------------------------------------------------------------

.. code:: python

   # Synchronous version
   try:
       result = getSomething()
   except:
       log.err()
   else:
       doSomething(result)

   # Asynchronous version
   d = getSomething()
   d.addCallbacks(doSomething, log.err)


Call a function and use the result, recovering from a particular exception raised by the function
-------------------------------------------------------------------------------------------------

.. code:: python

   # Synchronous version
   try:
       result = getSomething()
   except SomeException:
       result = 42
   doSomething(result)

   # Asynchronous version
   def _eb(f):
       f.trap(SomeException)
       return 42

   d = getSomething()
   d.addErrback(_eb)
   d.addCallback(doSomething)


Call a function and use the result, performing cleanup if an exception occurs
-----------------------------------------------------------------------------

.. code:: python

   # Synchronous version
   try:
       result = getSomething()
       doSomething(result)
   finally:
       cleanStuffUp()

   # Asynchronous version
   d = getSomething()
   d.addCallback(doSomething)
   d.addBoth(lambda ignored: cleanStuffUp())


Compose several functions
-------------------------

.. code:: python

   # Synchronous version
   result = getSomething()
   result2 = doStuff(result)
   result3 = doMoreStuff(result2)

   # Asynchronous version
   d = getSomething()
   d.addCallback(doStuff)
   d.addCallback(doMoreStuff)


If anyone has any suggestions for other examples I should add to this list,
feel free to leave a comment or `drop me a note`_, and I'll consider updating
the post.

.. _drop me a note: mailto:mithrandi@mithrandi.net
