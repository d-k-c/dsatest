

class Machine:
    """Machine being part of the benchtest"""

    def __init__(self, name, control):
        self.interfaces = list()
        self.name = name
        self.control = control
        self.allow_bridge_creation = True

    def __repr__(self):
        return "<Machine \"{.name}\">".format(self)

    def setBridgeCreationAllowed(self, val):
        self.allow_bridge_creation = val

    def addInterface(self, interface):
        self.interfaces.append(interface)

    ##################################################
    #           Wrap control functions               #
    ##################################################

    def exec(self, param):
        return self.control.exec(param)

    def getLastExitCode(self):
        return self.control.getLastExitCode()


    ##################################################
    # Network related functions, to be used in tests #
    ##################################################

    def up(self, interface):
        command = "ip link set {0} up".format(interface)
        self.control.execAndCheck(command)

    def down(self, interface):
        command = "ip link set {0} down".format(interface)
        self.control.execAndCheck(command)

    def addAddress(self, interface, address):
        command = "ip addr add {0} dev {1}".format(address, interface)
        self.control.execAndCheck(command)

    def delAddress(self, interface, address):
        command = "ip addr del {0} dev {1}".format(address, interface)
        self.control.execAndCheck(command)
