import unittest

from dsatest.bench import bench
from dsatest.tests.helpers import get_addresses, up_and_wait

@unittest.skipIf(not bench.links, "Empty link list")
class TestPingVlan(unittest.TestCase):

    VID_START = 0
    VID_END = 10

    def setUp(self):
        for link in bench.links:
            up_and_wait(link)
            link.host_if.flush_addresses()
            link.target_if.flush_addresses()


    def tearDown(self):
        for link in bench.links:
            link.host_if.down()
            link.target_if.down()


    @staticmethod
    def get_addr(index, append_prefix=False):
        subnet = "192.168.{}.0".format(10 + index)
        return get_addresses(subnet=subnet, prefix=24, append_prefix=append_prefix)


    def test_port_ping_vlan_all(self):
        for link in bench.links:
            host_if, target_if = link.host_if, link.target_if
            host_if.flush_addresses()
            target_if.flush_addresses()

            for i, vid in enumerate(range(TestPingVlan.VID_START, TestPingVlan.VID_END)):
                host_vlan = host_if.add_vlan(vid)
                target_vlan = target_if.add_vlan(vid)
                host_addr, target_addr = TestPingVlan.get_addr(i, append_prefix=True)
                host_vlan.add_address(host_addr)
                host_vlan.up()

                target_vlan.add_address(target_addr)
                target_vlan.up()

                _, addr = TestPingVlan.get_addr(i)
                host_vlan.ping(addr, count=1, deadline=10)

                host_vlan.flush_addresses()
                target_vlan.flush_addresses()
                host_vlan.down()
                target_vlan.down()
