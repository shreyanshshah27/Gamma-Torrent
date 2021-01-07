__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import errno
import logging
import random
import select
import socket
import time
from threading import Thread

import message_d.keepalive as ka
import message_d.message as msg
import message_d.request as req
import message_d.choke as chk
import message_d.unchoke as unck
import message_d.handshake as hdsk
import message_d.have as hve
import message_d.cancel as cncl
import message_d.interested as intsd
import message_d.notinterested as nitsd
import message_d.piece as pic
import message_d.bitfield as btfd

import pieces_d.rarest_piece as rarest_piece
from pubsub import pub
import peers_d.peer as peer


class PeersManager(Thread):

    # creating a constructor for initializing variables
    def __init__(self, torrent, pieces_manager):
        Thread.__init__(self)
        self.peers = []
        self.torrent = torrent
        self.pieces_manager = pieces_manager
        self.rarest_pieces = rarest_piece.RarestPieces(pieces_manager)
        self.pieces_by_peer = [[0, []] for _ in range(pieces_manager.number_of_pieces)]
        self.is_active = True

        # Events
        pub.subscribe(self.peer_requests_piece, 'PeersManager.PeerRequestsPiece')
        pub.subscribe(self.peers_bitfield, 'PeersManager.updatePeersBitfield')

    def peer_requests_piece(self, request=None, peer=None):
        if not request or not peer:
            print("\033[91m [!] Error : empty request/peer message\033[00m")

        piece_index, block_offset, block_length = request.piece_index, request.block_offset, request.block_length

        block = self.pieces_manager.get_block(piece_index, block_offset, block_length)
        if block:
            piece = msg.Piece(piece_index, block_offset, block_length, block).to_bytes()
            peer.send_to_peer(piece)
            print("\033[96m [+] Sent piece index \033[00m{} \033[96mto peer : \033[00m{}".format(request.piece_index, peer.ip))

    def peers_bitfield(self, bitfield=None):
        for i in range(len(self.pieces_by_peer)):
            if bitfield[i] == 1 and peer not in self.pieces_by_peer[i][1] and self.pieces_by_peer[i][0]:
                self.pieces_by_peer[i][1].append(peer)
                self.pieces_by_peer[i][0] = len(self.pieces_by_peer[i][1])

    # sending any random peer who meets the conditions
    def get_random_peer_having_piece(self, index):
        ready_peers = []

        for peer in self.peers:
            # conditions for selecting a peer is that it should be eligible, unchoked, interested to share and should contain the piece
            if peer.is_eligible() and peer.is_unchoked() and peer.am_interested() and peer.has_piece(index):
                ready_peers.append(peer)

        return random.choice(ready_peers) if ready_peers else None

    def has_unchoked_peers(self):
        for peer in self.peers:
            if peer.is_unchoked():
                return True
        return False

    def unchoked_peers_count(self):
        cpt = 0
        for peer in self.peers:
            if peer.is_unchoked():
                cpt += 1
        return cpt


    @staticmethod
    def _read_from_socket(sock):
        data = b''

        while True:
            try:
                # Receives 4096 bytes and returns 0 when the string is empty.
                buff = sock.recv(4096)
                if len(buff) <= 0:
                    break

                data += buff                # concatnating the content of buffer to data.
            except socket.error as e:
                err = e.args[0]
                if err != errno.EAGAIN or err != errno.EWOULDBLOCK:
                    logging.debug(" [!] Error No : {}".format(err))
                break
            except Exception:
                logging.exception(" [!] Recv failed")
                break

        return data

    # thread.run function
    def run(self):
        # if client is active, it will receive data from the socket
        while self.is_active:
            read = [peer.socket for peer in self.peers]
            read_list, _, _ = select.select(read, [], [], 1)

            for socket in read_list:
                # getting the peer having same socket
                peer = self.get_peer_by_socket(socket)

                # if the peer is not healthy then remove the peer.
                if not peer.healthy:
                    self.remove_peer(peer)
                    continue

                try:
                    # getting payload data from the socket.
                    payload = self._read_from_socket(socket)
                except Exception as e:
                    printf("\033[91m [!] Error : Recv failed \033[00m%s" % e.__str__())
                    self.remove_peer(peer)
                    continue
                
                # total payload added
                peer.read_buffer += payload
                
                for message in peer.get_messages():
                    self._process_new_message(message, peer)

    def _do_handshake(self, peer):
        try:
            # creating the info hash to the peer
            handshake = hdsk.Handshake(self.torrent.info_hash)
            peer.send_to_peer(handshake.to_bytes())
            print("\033[92m [+] New peer added : %s" % peer.ip)
            return True

        except Exception:
            print("\033[91m [!] Error : Sending Handshake message\033[00m")

        return False

    # adding peers to the list after doing handshake
    def add_peers(self, peers):
        for peer in peers:
            if self._do_handshake(peer):
                self.peers.append(peer)
            else:
                print("\033[91m [!] Error : Doing Handshake\033[00m")

    def remove_peer(self, peer):
        if peer in self.peers:
            try:
                peer.socket.close()
            except Exception:
                print("\033[91m [!] Error : Failed to Remove Peers\033[00m")

            self.peers.remove(peer)

        # for rarest_piece in self.rarest_pieces.rarest_pieces:
        #    if peer in rarest_piece["peers"]:
        #        rarest_piece["peers"].remove(peer)

    def get_peer_by_socket(self, socket):
        for peer in self.peers:
            if socket == peer.socket:
                return peer

        raise Exception("\033[91m [!] Error : Peer not present in peer_list \033[00m")

    def _process_new_message(self, new_message: msg.Message, peer: peer.Peer):
        if isinstance(new_message, hdsk.Handshake) or isinstance(new_message, ka.KeepAlive):
            logging.error("\033[96m [!] Error : Handshake or Keep-ALive should have already been handled\033[00m")

        elif isinstance(new_message, chk.Choke):
            peer.handle_choke()

        elif isinstance(new_message, unck.UnChoke):
            peer.handle_unchoke()

        elif isinstance(new_message, intsd.Interested):
            peer.handle_interested()

        elif isinstance(new_message, nitsd.NotInterested):
            peer.handle_not_interested()

        elif isinstance(new_message, hve.Have):
            peer.handle_have(new_message)

        elif isinstance(new_message, btfd.BitField):
            peer.handle_bitfield(new_message)

        elif isinstance(new_message, req.Request):
            peer.handle_request(new_message)

        elif isinstance(new_message, pic.Piece):
            peer.handle_piece(new_message)

        elif isinstance(new_message, cncl.Cancel):
            peer.handle_cancel()

        elif isinstance(new_message, port.Port):
            peer.handle_port_request()

        else:
            logging.error("\033[91m [!] Error : Unknown message Received \033[00m")
