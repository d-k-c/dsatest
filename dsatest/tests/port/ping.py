
import unittest

from dsatest.bench import bench
from dsatest.tests.helpers import get_addresses, up_and_wait

@unittest.skipIf(not bench.links, "Empty link list")
class TestPing(unittest.TestCase):

    @staticmethod
    def get_addr(offset, append_prefix=True):
        """generate addresses, starting from subnet 192.168.10.0, and increment
        the third number for each pair of interfaces"""
        subnet = "192.168.{}.0".format(offset + 10)
        return get_addresses(subnet=subnet, prefix=24, append_prefix=append_prefix)

    def setUp(self):
        links = bench.links

        for i, link in enumerate(links):
            host_addr, target_addr = self.get_addr(i)
            up_and_wait(link)
            link.host_if.flush_addresses()
            link.host_if.add_address(host_addr)
            link.target_if.flush_addresses()
            link.target_if.add_address(target_addr)


    def tearDown(self):
        links = bench.links

        for i, link in enumerate(links):
            host_addr, target_addr = self.get_addr(i)
            link.host_if.del_address(host_addr)
            link.host_if.down()
            link.target_if.del_address(target_addr)
            link.target_if.down()


    def test_port_ping_all(self):
        for i, link in enumerate(bench.links):
            _, target_addr = self.get_addr(i, append_prefix=False)
            link.host_if.ping(target_addr, count=1, deadline=10)
