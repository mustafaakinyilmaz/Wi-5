agent_click_template = """
// This is the scheme:
//
//            TAP interface 'ap' in the machine that runs Click
//                   | ^
// from host         | |      to host
//                   v |
//             --------------
//            |    click     |
//             --------------
//             | ^        | ^
// to device   | |        | | to device 
//             V |        V |
//            'mon0'     'mon1'    interfaces in the machine that runs Click. They must be in monitor mode
//

// call OdinAgent::configure to create and configure an Odin agent:
odinagent::OdinAgent(HWADDR {}, RT rates, CHANNEL {}, DEFAULT_GW {}, DEBUGFS /sys/kernel/debug/ieee80211/phy0/ath9k/bssid_extra, SSIDAGENT {}, DEBUG_ODIN {}, TX_RATE 108, TX_POWER 25, HIDDEN 0, MULTICHANNEL_AGENTS {}, DEFAULT_BEACON_INTERVAL 100, BURST_BEACON_INTERVAL 10, MEASUREMENT_BEACON_INTERVAL 100)

// send a ping to odinsocket every 2 seconds
TimedSource(2, "ping
")->  odinsocket::Socket(UDP, 192.168.6.219, 2819, CLIENT true)

// output 3 of odinagent goes to odinsocket
odinagent[3] -> odinsocket
rates :: AvailableRates(DEFAULT 12 18 24 36 48 72 96 108);	// wifi rates in multiples of 500kbps. This will be announced in the beacons sent by the AP
control :: ControlSocket("TCP", 6777);
chatter :: ChatterSocket("TCP", 6778);


// ----------------Packets going down (AP to STA)
// I don't want the ARP requests from the AP to the stations to go to the network device
//so click is in the middle and answers the ARP to the host on behalf of the station
//'ap' is a Linux tap device which is instantiated by Click in the machine.
//FromHost reads packets from 'ap'
// The arp responder configuration here doesnt matter, odinagent.cc sets it according to clients
FromHost(ap, HEADROOM 50)
  -> fhcl :: Classifier(12/0806 20/0001, -)
				// 12 means the 12th byte of the eth frame (i.e. ethertype)
				// 0806 is the ARP ethertype, http://en.wikipedia.org/wiki/EtherType
				// 20 means the 20th byte of the eth frame, i.e. the 6th byte of the ARP packet: 
				// "Operation". It specifies the operation the sender is performing: 1 for request, 2 for reply.
  -> fh_arpr :: ARPResponder(192.168.1.11 74:F0:6D:20:D4:74) 	// looking for an STA's ARP: Resolve STA's ARP
  -> ToHost(ap)

// Anything from host that is not an ARP request goes to the input 1 of Odin Agent
fhcl[1]
  -> [1]odinagent

// Not looking for an STA's ARP? Then let it pass.
fh_arpr[1]
  -> [1]odinagent

// create a queue 'q' for transmission of packets by the primary interface (mon0) and connect it to SetTXRate-RadiotapEncap
q :: Queue(50)
  -> SetTXRate (108)	// e.g. if it is 108, this means 54Mbps=108*500kbps
  -> RadiotapEncap()
  -> to_dev :: ToDevice (mon0);

  odinagent[2]
  -> q

// create a queue 'q2' for transmission of packets by the secondary interface (mon1) and connect it to SetTXRate-RadiotapEncap
q2 :: Queue(50)
  -> SetTXRate (108)	// e.g. if it is 108, this means 54Mbps=108*500kbps
  -> RadiotapEncap()
  -> to_dev2 :: ToDevice (mon1);


odinagent[4]
  -> q2

// ----------------Packets coming up (from the STA to the AP) go to the input 0 of the Odin Agent
from_dev :: FromDevice(mon0, HEADROOM 50)
  -> RadiotapDecap()
  -> ExtraDecap()
  -> phyerr_filter :: FilterPhyErr()
  -> tx_filter :: FilterTX()
  -> dupe :: WifiDupeFilter()	// Filters out duplicate 802.11 packets based on their sequence number
								// click/elements/wifi/wifidupefilter.hh
  -> [0]odinagent

// ----------------Packets coming up (from the STA to the AP) go to the input 0 of the Odin Agent
from_dev1 :: FromDevice(mon1, HEADROOM 50)
  -> RadiotapDecap()
  -> ExtraDecap()
  -> phyerr_filter1 :: FilterPhyErr()
  -> tx_filter1 :: FilterTX()
  -> dupe1 :: WifiDupeFilter()	// Filters out duplicate 802.11 packets based on their sequence number
								// click/elements/wifi/wifidupefilter.hh
  -> [2]odinagent
odinagent[0]
  -> q

// Data frames
// The arp responder configuration here does not matter, odinagent.cc sets it according to clients
odinagent[1]
  -> decap :: WifiDecap()	// Turns 802.11 packets into ethernet packets. click/elements/wifi/wifidecap.hh
  -> RXStats				// Track RSSI for each ethernet source.
							// Accumulate RSSI, noise for each ethernet source you hear a packet from.
							// click/elements/wifi/rxstats.hh
  -> arp_c :: Classifier(12/0806 20/0001, -)
				// 12 means the 12th byte of the eth frame (i.e. ethertype)
				// 0806 is the ARP ethertype, http://en.wikipedia.org/wiki/EtherType
				// 20 means the 20th byte of the eth frame, i.e. the 6th byte of the ARP packet: 
				// "Operation". It specifies the operation the sender is performing: 1 for request
  -> arp_resp::ARPResponder ({} {}) // ARP fast path for STA
									// the STA is asking for the MAC address of the AP
									// add the IP of the AP and the BSSID of the LVAP corresponding to this STA
  -> [1]odinagent

// Non ARP packets. Re-write MAC address to
// reflect datapath or learning switch will drop it
arp_c[1]
  -> ToHost(ap)

// Click is receiving an ARP request from a STA different from its own STAs
// I have to forward the ARP request to the host without modification
// ARP Fast path fail. Re-write MAC address (without modification)
// to reflect datapath or learning switch will drop it
arp_resp[1]
  -> ToHost(ap)"""