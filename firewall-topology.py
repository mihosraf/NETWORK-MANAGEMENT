#!/usr/bin/python

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call
from mininet.node import RemoteController, OVSSwitch
from mininet.util import quietRun, errRun
from mininet.util import dumpNodeConnections

def myNetwork():

    net = Mininet_wifi( controller=RemoteController,link=wmediumd,wmediumd_mode=interference,ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    
    c1 = net.addController('c1', ip='192.168.1.12',protocol='tcp',port=6633)

    info( '*** Add switches/APs\n')
    ap2 = net.addAccessPoint('ap2',  ssid='ap2-ssid',channel='1', mode='g', position='590,340,0')
    s1 = net.addSwitch('s1')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid',channel='1', mode='g', position='270,339,0')

    info( '*** Add hosts/stations\n')
    sta2 = net.addStation('sta2', ip='10.0.0.2',position='320,480,0')
    sta4 = net.addStation('sta4', ip='10.0.0.4',position='730,470,0')
    sta1 = net.addStation('sta1', ip='10.0.0.1',position='150,470,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3',position='540,470,0')

    net.configureWifiNodes()
    info( '*** Add links\n')
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap2, sta3)
    net.addLink(ap2, sta4)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap2').start([c1])
    net.get('s1').start([c1])
    net.get('ap1').start([c1])

    info( '*** Post configure nodes\n')
    print "Dumping host connections"
    dumpNodeConnections(net.stations)
    print "Testing network connectivity"
    print sta4.cmd('ping -c5 %s' % sta2.IP())
    print "Applying Rule now"
    ap1.cmd("ovs-ofctl add-flow ap1 priority=65535,ip,nw_dst=10.0.0.2,actions=drop")
    print " Ping again"
    print sta4.cmd('ping -c5 %s' % sta2.IP())

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
