__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import logging

import requests
from bcoding import bdecode
import tracker_d.socket_address as socket_address

class HttpScrapper(object):

    def __init__(self, torrent, tracker, dict_sock_addr):
        # loading the parameters for HTTP scrapper
        params = {
            'info_hash': torrent.info_hash,
            'peer_id': torrent.peer_id,
            'uploaded': 0,
            'downloaded': 0,
            'port': 6881,
            'left': torrent.total_length,
            'event': 'started'
        }
        self.dict_sock_addr = dict_sock_addr

        try:
            # HTTP : GET requesting the tracker link for the list of peers
            answer_tracker = requests.get(tracker, params=params, timeout=5)

            # decoding the response content
            list_peers = bdecode(answer_tracker.content)

            # for each peer, create a socket
            for p in list_peers['peers']:
                s = socket_address.SockAddr(p['ip'], p['port'])
                self.dict_sock_addr[s.__hash__()] = s

        except Exception as e:
            logging.exception("HTTP scraping failed: %s" % e.__str__())
        
    def get_dict_sock_addr(self):
        return self.dict_sock_addr
