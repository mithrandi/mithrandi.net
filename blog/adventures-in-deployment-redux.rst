.. title: Adventures in deployment, redux
.. slug: adventures-in-deployment-redux
.. date: 2018-01-19 21:52:04 UTC
.. tags: tech,rancher,docker,kubernetes,drone
.. category: 
.. link: 
.. description: 
.. type: text

Just a brief update: I've moved on from the hackish deployment strategy
described in an `older post`_; we now have `Drone`_ for CI building Docker images,
pushing them to a registry, and deploying them on `Rancher`_. You can see an
example of the `Drone pipeline`_ to do this in our GitHub repos.

This is all I'm going to say on the topic, because that's all there really is
to it. If you're using Kubernetes, I strongly suggest you look into `Weave Flux`_
for deployment; this is eventually where I want to end up, but migrating to
Kubernetes is hard for us at the moment.

.. _older post: https://mithrandi.net/blog/2015/06/adventures-in-deployment-with-propellor-docker-and-fabric/
.. _Drone: http://docs.drone.io/
.. _Rancher: https://rancher.com/
.. _Drone pipeline: https://github.com/fusionapp/clj-documint/blob/e254a1ab1eeba58f53d815d7a16514179d6fe57b/.drone.yml
.. _Weave Flux: https://github.com/weaveworks/flux
