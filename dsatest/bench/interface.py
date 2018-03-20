
class BaseInterface(object):
    """
    Network interface on a Machine. The name must be a string on which
    commands can be operated (like `ip link`)
    """

    def __init__(self, name, machine, switch=None, port_id=None):
        self.name = name
        self.machine = machine
        self.switch = switch
        self.port_id = port_id

    def __repr__(self):
        if self.switch:
            return ("<BaseInterface {s.machine.name} "
                    "{s.name} {s.switch.name}.{s.port_id}>".format(s=self))

        return "<Interface {s.machine.name} {s.name}>".format(s=self)

    def up(self):
        self.machine.up(self.name)

    def down(self):
        self.machine.down(self.name)

    def add_address(self, address):
        self.machine.add_address(self.name, address)

    def del_address(self, address):
        self.machine.del_address(self.name, address)

    def flush_addresses(self):
        self.machine.flush_addresses(self.name)

    def ping(self, destination, count=None, deadline=None):
        self.machine.ping(destination, from_if=self.name, count=count, deadline=deadline)

    def arp_get(self, address):
        return self.machine.arp_get(address, self.name)

class Vlan(BaseInterface):

    def __init__(self, parent_if, vid):
        # name will be set in self.name in parent constructor
        name = "{}.{}".format(parent_if.name, vid)
        super().__init__(self, name, parent_if.machine,
                         parent_if.switch, parent_if.port_id)
        self.parent = parent_if
        self.vid = vid

    def setup(self):
        return self.parent.machine.add_vlan(self.name, self.parent.name, self.vid)

    def teardown(self):
        return self.parent.machine.del_vlan(self.name)

class Interface(BaseInterface):

    def __init__(self, name, machine, switch=None, port_id=None):
        super().__init__(name, machine, switch, port_id)
        self.vlans = dict()

    def __del__(self):
        # make sure we get rid of underlying VLANs
        for vlan in self.vlans.values():
            vlan.teardown()

    def add_vlan(self, vid):
        vlan = Vlan(self, vid)
        vlan.setup()
        self.vlans[vid] = vlan
        return vlan

    def del_vlan(self, vid):
        self.vlans[vid].teardown()
        del self.vlans[vid]
