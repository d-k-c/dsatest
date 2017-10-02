
from squidsa.parser import BenchParser, TargetParser
from .control import LocalControl, SSHControl
from .interface import Interface
from .link import Link
from .machine import Machine

class Bench:

    def __init__(self):
        self.is_setup = False

    def setup(self, bench_config_file):
        bench_parser = BenchParser(bench_config_file)
        target_parser = TargetParser(bench_parser.target_name)
        host_ctrl = LocalControl()
        username = getattr(bench_parser, "ssh_username", None)
        password = getattr(bench_parser, "ssh_password", None)
        keyfile = getattr(bench_parser, "ssh_keyfile", None)
        target_ctrl = SSHControl(bench_parser.ssh, username=username,
                                 password=password, keyfile=keyfile)

        # Create machines involved in the test bench
        self.target = Machine("Target", target_ctrl)
        self.host = Machine("Host", host_ctrl)

        self.links = list()
        self.incomplete_links = list()
        for link_name, link in bench_parser.links.items():
            if link.is_incomplete():
                self.incomplete_links.append(link_name)
                continue

            switch, port = target_parser.get_interface_info(link_name)

            host_if = Interface(link.host, self.host)
            target_if = Interface(link.target, self.target, switch, port)

            self.host.addInterface(host_if)
            self.target.addInterface(target_if)

            l = Link(link_name, host_if, target_if)
            self.links.append(l)

            self.is_setup = True


    def connect(self, dry_run=False):
        if not dry_run:
            self.target.control.connect()

    def disconnect(self, dry_run=False):
        if not dry_run:
            self.target.control.disconnect()

