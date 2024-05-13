# Portfolio
README

This repository contains code for setting up a network topology using the Mininet network emulator and implementing a simple routing algorithm using the POX OpenFlow controller.

The topology consists of a core switch connected to four edge switches, each connected to various hosts representing different departments in a company. The IP addresses and MAC addresses for each host are specified in the code.

To run the network, run the configure() function in the "final_topo.py" file. This will start the Mininet network and open a CLI console for interacting with the network.

To implement the routing algorithm, run the "pox.py" file with the "routing" module specified. This will start the POX OpenFlow controller and activate the routing logic.

Note that the routing algorithm in this code is a simple one that forwards packets between switches based on the IP address of the destination host. More sophisticated routing algorithms could be implemented by modifying the "Routing" class in the "routing.py" file.

This code is provided as a starting point for creating and experimenting with network topologies using Mininet and POX. Feel free to modify and extend the code to suit your needs.
