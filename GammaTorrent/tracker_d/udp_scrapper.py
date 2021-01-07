__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


import ipaddress
import logging
import socket
from urllib.parse import urlparse

import requests
import message_d.udptracker as udptracker
from peers_d import peers_manager
import tracker_d.socket_address as socket_address

class UdpScrapper(object):

    def __init__(self, torrent, announce, dict_sock_addr):
        self.torrent = torrent
        
        # separating components of the tracker url.
        parsed = urlparse(announce)
        self.dict_sock_addr = dict_sock_addr

        # creating a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # setting socket options
        # SOL_SOCKET - int which specifies the level of the socket for UDP
        # REUSEADDR - reuse of local addresses should be allowed by the rules used in validating addresses supplied to bind()
        # IPPROTO_TCP - level for TCP socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(4)
        ip, port = socket.gethostbyname(parsed.hostname), parsed.port

        # can only request if the IP address is public
        if ipaddress.ip_address(ip).is_private:
            return

        # connection UDP Tracker and creating tracker input having transaction_id, connection_id and action
        tracker_connection_input = udptracker.UdpTrackerConnection()

        # sending data as message to the created socket and getting the response.
        response = self.send_message((ip, port), sock, tracker_connection_input)

        if not response:
            raise Exception("\033[95m [?] No response for UdpTrackerConnection\033[00m")
        
        # decoding and defragmenting the response from the tracker into different elements
        tracker_connection_output = udptracker.UdpTrackerConnection()
        tracker_connection_output.from_bytes(response)

        # Announcing the packet
        tracker_announce_input = udptracker.UdpTrackerAnnounce(self.torrent.info_hash, tracker_connection_output.conn_id,self.torrent.peer_id)
        # sending data as message to the created socket and getting the response.
        response = self.send_message((ip, port), sock, tracker_announce_input)

        if not response:
            raise Exception("\033[95m [?] No response for UdpTrackerAnnounce\033[00m")
        
        # announcing the output
        tracker_announce_output = udptracker.UdpTrackerAnnounceOutput()
        # getting content from the enxrypted response
        tracker_announce_output.from_bytes(response)

        for ip, port in tracker_announce_output.list_sock_addr:
            sock_addr = socket_address.SockAddr(ip, port)

            if sock_addr.__hash__() not in self.dict_sock_addr:
                self.dict_sock_addr[sock_addr.__hash__()] = sock_addr

        print("\033[95m [>] Got \033[00m%d\033[95m peers\033[00m" % len(self.dict_sock_addr))
        
    def get_dict_sock_addr(self):
        return self.dict_sock_addr

    def send_message(self, conn, sock, tracker_message):
        # Encoding the message in a string representation
        message = tracker_message.to_bytes()
        trans_id = tracker_message.trans_id
        action = tracker_message.action
        size = len(message)

        # sending the encoded message to the given conn = (ip and port)
        sock.sendto(message, conn)

        try:
            # reading response from the socket which returns the data.
            response = peers_manager.PeersManager._read_from_socket(sock)
        except socket.timeout as e:
            logging.debug("\033[91m [!] Timeout : \033[00m%s" % e)
            return
        except Exception as e:
            print("\033[91m [!] Error : Message was not sent successfully : \033[00m%s" % e.__str__())
            return

        if len(response) < size:
            print("\033[91m [!] Error : Did not get full message.\033[00m")

        if action != response[0:4] or trans_id != response[4:8]:
            print("\033[91m [!] Transaction-ID did not match\033[00m")

        # returns the data if there is not issue as mentioned above.
        return response
