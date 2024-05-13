#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):

    #add switches 
    switch1 = self.addSwitch('s1')
    switch2 = self.addSwitch('s2')
    switch3 = self.addSwitch('s3')
    switch4 = self.addSwitch('s4')
    core = self.addSwitch('s0')
    
    self.addLink(core, switch1, port1 = 31, port2 = 4)
    self.addLink(core, switch2, port1 = 32, port2 = 5)
    self.addLink(core, switch3, port1 = 33, port2 = 6)
    self.addLink(core, switch4, port1 = 34, port2 = 7)
    #Sales Department
    Laptop1 = self.addHost('Laptop1',mac="00:00:00:00:00:10", ip='10.0.0.10/24',defaultRoute="Laptop1-eth5")
    Printer = self.addHost('Printer',mac="00:00:00:00:00:09", ip='10.0.0.9/24',defaultRoute="Printer-eth5")
    Laptop2 = self.addHost('Laptop2',mac="00:00:00:00:00:08", ip='10.0.0.8/24',defaultRoute="Laptop2-eth5")


    self.addLink(Laptop1, switch1, port1 = 5, port2 = 1)
    self.addLink(Printer, switch1, port1 = 5, port2 = 2)
    self.addLink(Laptop2, switch1, port1 = 5, port2 = 3)

    #OT Department
    Workstation1 = self.addHost('ws1',mac="00:00:00:00:00:07", ip='10.0.3.7/24', defaultRoute="ws1-eth5")
    Workstation2 = self.addHost('ws2',mac="00:00:00:00:00:06", ip='10.0.3.6/24', defaultRoute="ws2-eth5")



    self.addLink(Workstation1, switch2, port1 = 5, port2 = 1)
    self.addLink(Workstation2, switch2, port1 = 5, port2 = 2)

    #IT department
    Workstation3 = self.addHost('ws3',mac="00:00:00:00:00:05", ip='10.0.2.5/24', defaultRoute="ws3-eth5")
    Workstation4 = self.addHost('ws4',mac="00:00:00:00:00:04", ip='10.0.2.4/24', defaultRoute="ws4-eth5")


    self.addLink(Workstation3, switch3, port1 = 5, port2 = 1)
    self.addLink(Workstation4, switch3, port1 = 5, port2 = 2)

    #Data Center
    Server2 = self.addHost('Server2',mac="00:00:00:00:00:01", ip='10.0.1.1/24', defaultRoute="Server2-eth5")
    webServer = self.addHost('webServer',mac="00:00:00:00:00:02", ip='10.0.1.2/24', defaultRoute="webServer-eth5")
    dnsServer = self.addHost('dnsServer',mac="00:00:00:00:00:03", ip='10.0.1.3/24', defaultRoute="dnsServer-eth5")

    self.addLink(Server2, switch4, port1 = 5, port2 = 1)
    self.addLink(webServer, switch4, port1 = 5, port2 = 2)
    self.addLink(dnsServer, switch4, port1 = 5, port2 = 3)





def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  # use static ARP
  net.staticArp() 
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()