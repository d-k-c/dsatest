
import unittest

from dsatest.bench import Bridge, Interface, bench

class TestSanity(unittest.TestCase):

    def test_bench_is_not_none(self):
        self.assertTrue(bench is not None)

    def test_bench_setup(self):
        self.assertTrue(bench.is_setup)

    def test_links_is_iterable(self):
        self.assertTrue(iter(bench.links))

    def test_link_has_interfaces(self):
        for link in bench.links:
            self.assertIsInstance(link.host_if, Interface)
            self.assertIsInstance(link.target_if, Interface)

    def test_interface_member(self):
        for link in bench.links:
            interface = link.target_if
            self.assertIsInstance(interface.name, str)
            self.assertIsInstance(interface.port_id, str)

    def test_link_names(self):
        links = bench.links
        if len(links) == 0:
            self.skipTest("Empty link list")

        for l in links:
            host = l.host_if.name
            target = l.target_if.name
            self.assertIsInstance(host, str)
            self.assertIsInstance(target, str)
            self.assertTrue(len(host) > 0)
            self.assertTrue(len(target) > 0)

    def test_interface_api(self):
        for link in bench.links:
            ifs = [ link.host_if, link.target_if ]
            for interface in ifs:
                self.assertTrue(hasattr(interface, "up"))
                self.assertTrue(hasattr(interface, "down"))
                self.assertTrue(hasattr(interface, "addAddress"))
                self.assertTrue(hasattr(interface, "delAddress"))

    def test_machine_api(self):
        machs = [ bench.host, bench.target ]
        for mach in machs:
            self.assertTrue(hasattr(mach, "up"))
            self.assertTrue(hasattr(mach, "down"))
            self.assertTrue(hasattr(mach, "addAddress"))
            self.assertTrue(hasattr(mach, "delAddress"))
            self.assertTrue(hasattr(mach, "addBridge"))
            self.assertTrue(hasattr(mach, "delBridge"))
            self.assertTrue(hasattr(mach, "ping"))

    def test_bridge_api(self):
        b = Bridge("br0", None)
        self.assertTrue(hasattr(b, "addInterface"))
        self.assertTrue(hasattr(b, "delInterface"))
        # it should also have the same functions as regular Interface
        self.assertTrue(hasattr(b, "up"))
        self.assertTrue(hasattr(b, "down"))
        self.assertTrue(hasattr(b, "addAddress"))
        self.assertTrue(hasattr(b, "delAddress"))

    def test_sanity_echo_target(self):
        ret, stdout, stderr = bench.target.exec("echo -n 'Hello World'")
        self.assertEqual(stdout.strip(), "Hello World")
        self.assertEqual(stderr.strip(), "")

    def test_sanity_echo_target_stderr(self):
        ret, stdout, stderr = bench.target.exec("echo -n 'Hello World' >&2")
        self.assertEqual(stdout.strip(), "")
        self.assertEqual(stderr.strip(), "Hello World")

    def test_sanity_echo_host(self):
        ret, stdout, stderr = bench.host.exec("echo -n 'Hello World'")
        self.assertEqual(stdout.strip(), "Hello World")
        self.assertEqual(stderr.strip(), "")

    def test_sanity_echo_host_stderr(self):
        ret, stdout, stderr = bench.host.exec("echo -n 'Hello World' >&2")
        self.assertEqual(stdout.strip(), "")
        self.assertEqual(stderr.strip(), "Hello World")

    def test_sanity_stats(self):
        interface = bench.links[0].target_if
        interface.stats.snapshot()
        print(interface.stats.rx_octets)
