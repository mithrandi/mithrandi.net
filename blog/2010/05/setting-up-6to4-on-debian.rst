There are already any number of blog posts, wiki pages, and so on spread all
over the internet that cover this topic. However, all of them seem to be based
on outdated information, making the instructions and configuration involved
more convoluted than necessary. So, without further ado, here's the easy way to
set 6to4 up on Debian.

First, you will need to calculate your 6to4 IPv6 address prefix, which is based
on the IPv4 address of the host you are using as your 6to4 router. For example,
if your router's public address is 10.10.10.1 (this is NOT actually a public
address)::

   $ ipv6calc --action conv6to4 10.10.10.1</code>
   No input type specified, try autodetection...found type: ipv4addr
   No output type specified, try autodetection...found type: ipv6addr
   2002:a0a:a01::

Add 1 to the end of this to obtain your router's address, ``2002:a0a:a01::1``
in this case. Next, you will need to add an entry for the tunnel to
``/etc/network/interfaces``::

   auto tun6to4
   iface tun6to4 inet6 v4tunnel
       address 2002:a0a:a01::1
       netmask 16
       gateway ::192.88.99.1
       endpoint any
       local 10.10.10.1
       ttl 255

Replace ``2002:a0a:a01::1`` with your IPv6 router address, and replace
``10.10.10.1`` with your public IPv4 address; ``192.88.99.1`` is the anycast
address for the nearest 6to4 gateway, so leave that alone unless you know what
you're doing. You can now bring the tunnel up with ``ifup tun6to4``, and you
should have IPv6 connectivity.

UPDATE: Derek points out `this handy site`_ in the comments that will calculate
some of the above for you automatically.

.. _this handy site: http://debian6to4.gielen.name/

Your 6to4 prefix is a /48, allowing you to allocate 2 ^ 16 (65536) /64 subnets
below this. In the usual case of a small home / business network, you won't
need more than one of these, so just pick one to use for your network. For
example, if we pick ``DEAD``, the network prefix would be
``2002:a0a:a01:dead::/64``. You can manually assign addresses to the
hosts on your network, but it will probably be easier to do EUI64-based
autoconfiguration; this allows each host to automatically select an address
based on their MAC address when they receive a router advertisement. In order
to send router advertisements, you will need to install ``radvd``, and
then put something like the following in ``/etc/radvd.conf``::

   interface eth0
   {
       AdvSendAdvert on;
       prefix 0:0:0:DEAD::/64
       {
           AdvOnLink on;
           AdvAutonomous on;
           Base6to4Interface ppp0;
       };
   };

Replace eth0 with the name of your network interface; this is the interface on
which router advertisements will be broadcast. You could hardcode your 6to4
prefix, but it's more convenient to use the ``Base6to4Interface``
option to have ``radvd`` calculate it for you; replace
``ppp0`` with the interface for your public internet connection, and
the prefix will be altered accordingly. If your public internet connection is
not on a separate interface, then just remove this option, and replace the
prefix address with the full address as shown earlier.

Your hosts should now have performed EUI64-based autoconfiguration and
configured a public IPv6 address for themselves, unless you have disabled this
for some reason. If you need to manually calculate the auto-configured address
for a particular host, you can do so given its MAC address::

   $ ipv6calc --action prefixmac2ipv6 --in prefix+mac --out ipv6 \
       2002:a0a:a01:dead::/64 11:22:33:44:55:66
   2002:a0a:a01:dead:1322:33ff:fe44:5566/64

Replace the prefix and MAC address with your own, of course. If IPv6 privacy
extensions are enabled, this address will be assigned to the network interface,
but an additional temporary anonymous address will be assigned based on a
randomly-generated identifier. The temporary address will be used for outgoing
connections, thus avoiding exposing your MAC address to every host you connect
to; the permanent address can still be used for incoming connections, allowing
you to use this address in DNS entries and so on. Privacy extensions will
typically be disabled by default on Linux-based hosts, and enabled on Windows
hosts.

There is usually no real reason to disable privacy extensions; however, there
is another feature enabled by default on Windows hosts that you may wish to
disable. This feature randomizes the identifier used for the permanent address,
separately from the temporary addresses assigned by privacy extensions. The
randomly generated identifier should be persisted, so the address will not
change, but it will bear no relation to the MAC address, thus preventing you
from being able to calculate it. If you wish to disable this feature, run the
following command with Administrator privileges::

   netsh interface ipv6 set global randomizeidentifiers=disabled

If you also wish to disable privacy extensions, you can use the following
command, but note that this is not necessary if you just want persistent
EUI64-based addresses::

   netsh interface ipv6 set privacy disabled
