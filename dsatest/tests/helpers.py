
import socket
import struct
import time

from dsatest.bench import Bridge, Link

def _expand_interfaces(interfaces, item, expand):
    if isinstance(item, Link):
        interfaces.extend((item.host_if, item.target_if))
    else:
        interfaces.append(item)

        if expand:
            if isinstance(item, Bridge):
                interfaces.extend(item.interfaces)


def up_and_wait(up_interfaces, monitored=None, expand=True):
    """
    Take an instance, or a list, of Interface, Bridge, or Link, and put it in
    the 'up' state, and wait for its operstate to become 'up'. One can wait on
    a different set of interfaces to become 'up' by passing
      monitored=[if1, if2]
    Note that by default, interfaces within a Bridge will also be up'ed when
    the bridge interface is up'ed. To prevent that, pass Expand=False.
    """
    interfaces = list()

    # accept a list or just one instance
    try:
        for item in up_interfaces:
            _expand_interfaces(interfaces, item, expand)
    except TypeError:
        _expand_interfaces(interfaces, up_interfaces, expand)

    for interface in interfaces:
        interface.up()

    if not monitored:
        monitored = interfaces

    timeout = 10
    while timeout:
        for interface in monitored:
            read_operstate_cmd = "cat /sys/class/net/{}/operstate".format(interface.name)
            ret, stdout, _ = interface.machine.execute(read_operstate_cmd)
            if ret == 0 and stdout == "up":
                monitored.remove(interface)

        if not monitored:
            return

        time.sleep(1)
        timeout = timeout - 1

    raise RuntimeError("some interfaces did not up within alloted period")


def get_addresses(subnet="192.168.10.0", prefix=24, offset=0, append_prefix=False):
    """return a pair of addresses to be used to configure host and target
    machines on the same subnet. By default, it will return the first two
    addresses in the subnet (excluding the base subnet address). This can
    be overriden by setting `offset`.

    >>> get_addresses()
    ['192.168.10.1', '192.168.10.2']
    >>> get_addresses(subnet="192.168.20.0")
    ['192.168.20.1', '192.168.20.2']
    >>> get_addresses(subnet="10.0.0.0", prefix=8)
    ['10.0.0.1', '10.0.0.2']
    >>> get_addresses(subnet="10.0.0.0", prefix=8, offset=256)
    ['10.0.1.1', '10.0.1.2']
    >>> get_addresses(append_prefix=True))
    ['192.168.10.1/24', '192.168.10.2/24']
    """
    subnet_mask = (1 << 32) - (1 << (32 - prefix))
    packed_ip = socket.inet_aton(subnet)
    subnet_base = struct.unpack("!L", packed_ip)[0] & subnet_mask

    addresses = []
    offset += 1 # start at the first address *after* the subnet address
    for suffix in range(offset, offset + 2):
        address = subnet_base + suffix
        address = socket.inet_ntoa(struct.pack('!L', address))
        if append_prefix:
            address = "{}/{}".format(address, prefix)
        addresses.append(address)

    return addresses[0], addresses[1]
