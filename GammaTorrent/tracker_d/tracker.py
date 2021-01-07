__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


import ipaddress
import logging
import socket
from urllib.parse import urlparse

from peers_d import peer
import requests
from bcoding import bdecode
import tracker_d.socket_address as socket_address
import tracker_d.http_scrapper as http_scrapper
import tracker_d.udp_scrapper as udp_scrapper


MAX_PEERS_TRY_CONNECT = 30
MAX_PEERS_CONNECTED = 8

"""
Please refer the following link to understand the flow
https://wiki.theory.org/BitTorrentSpecification#Tracker_HTTP.2FHTTPS_Protocol

"""

class Tracker(object):

    # constructor to initialize the variables
    def __init__(self, torrent):
        self.torrent = torrent
        self.threads_list = []
        self.connected_peers = {}
        self.dict_sock_addr = {}

    def get_peers_from_trackers(self):
        
        for i, tracker in enumerate(self.torrent.announce_list):
            # checking if connected peers doesn't exceed the maximum limit.
            if len(self.dict_sock_addr) >= MAX_PEERS_TRY_CONNECT:
                break

            tracker_url = tracker[0]

            # separating HTTP and UTP links and scrapping them
            if str.startswith(tracker_url, "http"):
                    hs = http_scrapper.HttpScrapper(self.torrent, tracker_url, self.dict_sock_addr)
                    self.dict_sock_addr = hs.get_dict_sock_addr()

            elif str.startswith(tracker_url, "udp"):
                    us=udp_scrapper.UdpScrapper(self.torrent, tracker_url, self.dict_sock_addr)
                    self.dict_sock_addr = us.get_dict_sock_addr()

            else:
                print("\033[91m [!] Currently we support only HTTP/UDP trackers..\nWe working on implementing support for : \033[00m%s " % tracker_url)
        
        # connect peer
        self.try_peer_connect()

        return self.connected_peers

    def try_peer_connect(self):
        print("\033[95m [>] Trying to connect to \033[00m%d\033[95m peer(s)\033[00m" % len(self.dict_sock_addr))
        # for every socket address, a new peer is joined
        for _, sock_addr in self.dict_sock_addr.items():
            if len(self.connected_peers) >= MAX_PEERS_CONNECTED:
                break
            
            
            new_peer = peer.Peer(int(self.torrent.number_of_pieces), sock_addr.ip, sock_addr.port)
            if not new_peer.connect():
                continue

            print('\033[92m [+] Connected to \033[00m%d \033[92m/\033[00m %d \033[92mpeers\033[00m' % (len(self.connected_peers) + 1, MAX_PEERS_CONNECTED))

            self.connected_peers[new_peer.__hash__()] = new_peer