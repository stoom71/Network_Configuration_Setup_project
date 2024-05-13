from pox.core import core

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet


    ICMP = packet.find("icmp")
    TCP = packet.find("tcp")
    IP = packet.find("ipv4")
    UDP = packet.find("udp")
    dstip = packet.payload.dstip.toStr()
    srcip = packet.payload.srcip.toStr()
    endport = 0

    if ICMP or TCP or UDP:
      if switch_id == 1:
        if ICMP:
          if IP.dstip == '10.0.0.10':
            endport = 1
          elif IP.dstip == '10.0.0.9':
            endport = 2
          elif IP.dstip == '10.0.0.8':
            endport = 3
          else:
            endport = 4
        elif UDP:
          if srcip.startswith("10.0.1.") and dstip.startswith("10.0.0."):
            endport = port_on_switch
            if port_on_switch == endport:
              if IP.dstip == '10.0.0.10':
                endport = 1
              elif IP.dstip == '10.0.0.9':
                endport = 2
              elif IP.dstip == '10.0.0.8':
                endport = 3
            else:
              endport = port_on_switch
          elif srcip.startswith("10.0.0.") and dstip.startswith("10.0.0."):
            endport = port_on_switch
            if port_on_switch == endport:
              if IP.dstip == '10.0.0.10':
                endport = 1
              elif IP.dstip == '10.0.0.9':
                endport = 2
              elif IP.dstip == '10.0.0.8':
                endport = 3
          else:
            endport = 4
              
      elif switch_id == 2:
        if ICMP or TCP:
          if IP.dstip == '10.0.3.7':
            endport = 1
          elif IP.dstip == '10.0.3.6':
            endport = 2
          else:
            endport = 5
      elif switch_id == 3:
        if ICMP or TCP:
          if IP.dstip == '10.0.2.5':
            endport = 1
          elif IP.dstip == '10.0.2.4':
            endport = 2
          else:
            endport = 6
      elif switch_id == 4:
        if TCP:
          if IP.dstip == '10.0.1.3':
            endport = 3
          elif IP.dstip == '10.0.1.2':
            endport = 2
          elif IP.dstip == '10.0.1.1':
            endport = 1
          else:
            endport = 7
        elif UDP:
          if srcip.startswith("10.0.0.") and dstip.startswith("10.0.1."):
            endport = port_on_switch
            if port_on_switch == endport:
              if IP.dstip == '10.0.1.1':
                endport = 1
              elif IP.dstip == '10.0.1.2':
                endport = 2
              elif IP.dstip == '10.0.1.3':
                endport = 3
            else:
              endport = port_on_switch
          elif srcip.startswith("10.0.1.") and dstip.startswith("10.0.1."):
            endport = port_on_switch
            if port_on_switch == endport:
              if IP.dstip == '10.0.1.1':
                endport = 1
              elif IP.dstip == '10.0.1.2':
                endport = 2
              elif IP.dstip == '10.0.1.3':
                endport = 3
            else:
              endport = port_on_switch
          else:
            endport = 7
      else:
        print(IP.dstip.toStr()[5])
        if IP.dstip.toStr()[5] == '0':
          if UDP:
            if port_on_switch == 34:
              endport = 31
          else:
            endport = 31
        elif IP.dstip.toStr()[5] == '3' and not UDP:
          endport = 32
        elif IP.dstip.toStr()[5] == '2' and not UDP:
          endport = 33
        elif IP.dstip.toStr()[5] == '1':
          if UDP:
            if port_on_switch == 31:
              endport = 34
          else:
            endport = 34
    print(endport)
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)

    msg.actions.append(of.ofp_action_output(port = endport))
    msg.data = packet_in
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
