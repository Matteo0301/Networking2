from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import subprocess


# Class that defines a topology
class MyTopo(Topo):

    def build(self):

        # templates for configuration parameters
        host_config = dict(inNamespace=True)
        link_config = dict()
        host_link_config = dict()

        # add switches
        for i in range(3):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % i, **sconfig)

        # add hosts
        for i in range(9):
            self.addHost("h%d" % i, **host_config)

        # add server
        self.addHost("server", **host_config)

        # Add links
        # Add switch links
        self.addLink("s0", "s1", **link_config)
        self.addLink("s2", "s1", **link_config)

        # Add clients-switch links
        self.addLink("h0", "s0", **host_link_config)
        self.addLink("h1", "s0", **host_link_config)
        self.addLink("h2", "s0", **host_link_config)
        self.addLink("h3", "s0", **host_link_config)
        self.addLink("h4", "s2", **host_link_config)
        self.addLink("h5", "s2", **host_link_config)
        self.addLink("h6", "s2", **host_link_config)
        self.addLink("h7", "s2", **host_link_config)
        self.addLink("h8", "s2", **host_link_config)
        self.addLink("server", "s1", **host_link_config)


if __name__ == "__main__":
    topo = MyTopo()
    net = Mininet(
        topo=topo,

        # We specify an external controller by passing the Controller object in the Mininet constructor
        # controller=RemoteController( 'c0', ip='127.0.0.1'),
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    # controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    # net.addController(controller)

    net.build()
    net.start()

    # subprocess.call("./initial_scenario.sh")

    CLI(net)
    net.stop()
