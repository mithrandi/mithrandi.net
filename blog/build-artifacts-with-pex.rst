.. title: Build artifacts with pex
.. slug: build-artifacts-with-pex
.. date: 2018-05-19 08:01:03 UTC
.. tags: tech,docker,drone,python,pex
.. category: 
.. link: 
.. description: 
.. type: text

For Continuous Integration in my Python application (as opposed to library)
projects, I generally want to run my tests as well as build a Docker image,
making use of the same artifacts and environment for both: I want to test what
I'm actually deploying, rather than something merely similar. Previously this meant doing ``pip install`` twice; once into a virtualenv to run the tests, then again in the Docker image build. Sharing the pip cache between these steps speeds things up a lot, but this still ends up using quite a bit of time on network roundtrips etc.

Now that `pex works with pypy`_, I have developed a slightly better workflow
for this. Briefly speaking, `Pex`_ is a tool for assembling a Python application
into a single runnable file that embeds the dependencies of the application; at
runtime, the dependencies are ziploaded or extracted to a temporary location as
necessary to run the application.

The workflow:

1. `Build a pex file`_.
2. `Run the tests`_ against the pex file.
3. `Copy the pex`_ into the Docker image.

This is similar to what I would do with a language like Go or Haskell that
would produce a single executable as part of the build process.

.. _pex works with pypy: https://github.com/pantsbuild/pex/issues/222#issuecomment-389387644
.. _pex: https://github.com/pantsbuild/pex
.. _Build a pex file: https://github.com/fusionapp/fusion-index/blob/b607b5359ad70da3eb4e8a360efd2d7e6b307940/.drone.yml#L23-L33
.. _Run the tests: https://github.com/fusionapp/fusion-index/blob/b607b5359ad70da3eb4e8a360efd2d7e6b307940/.drone.yml#L34
.. _Copy the pex: https://github.com/fusionapp/fusion-index/blob/master/Dockerfile#L3
