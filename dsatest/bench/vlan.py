
from .interface import BaseInterface

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
