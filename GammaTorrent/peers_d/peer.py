__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import time
import socket
import struct
import bitstring
from pubsub import pub
import logging

import message_d.message as message
import message_d.unchoke as unck
import message_d.handshake as hdsk
import message_d.interested as intrstd
import message_d.notinterested as notinterested
import message_d.message_exception as msgexcp
import message_d.keepalive as keepalive

class Peer(object):
    def __init__(self, number_of_pieces, ip, port=6881):    # initializing the variables 
        self.last_call = 0.0
        self.has_handshaked = False
        self.healthy = False
        self.read_buffer = b''                            
        self.socket = None
        self.ip = ip
        self.port = port
        self.number_of_pieces = number_of_pieces
        self.bit_field = bitstring.BitArray(number_of_pieces)
        self.state = {
            'am_choking': True,
            'am_interested': False,
            'peer_choking': True,
            'peer_interested': False,
        }

    def __hash__(self):
        return "%s:%d" % (self.ip, self.port)

    def connect(self):
        try:
            # Create a TCP/IP socket and Connect the socket to the port where the server is listening with timeout = 2s
            self.socket = socket.create_connection((self.ip, self.port), timeout=2)
            
            # setting a non-blocking socket
            self.socket.setblocking(0)
            print("\033[92m [+] Connected to peer ip: \033[00m %s \033[92m - port: \033[00m %s " % (self.ip, self.port))
            self.healthy = True

        except Exception as e:
            print("\033[93m [-] Failed to connect to peer (ip: \033[00m%s \033[93m - port: \033[00m%s \033[93m - \033[00m%s\033[93m) \033[00m" % (self.ip, self.port, e.__str__()))
            return False
            
        # if Connection is established.. Return true
        return True

    def send_to_peer(self, msg):
        try:
            self.socket.send(msg)
            self.last_call = time.time()
        except Exception as e:
            self.healthy = False
            print("\033[91m [!] Failed to send to peer : \033[00m%s" % e.__str__())

    def is_eligible(self):
        now = time.time()
        return (now - self.last_call) > 0.2

    def has_piece(self, index):
        return self.bit_field[index]

    def am_choking(self):
        return self.state['am_choking']

    def am_unchoking(self):
        return not self.am_choking()

    def is_choking(self):
        return self.state['peer_choking']

    def is_unchoked(self):
        return not self.is_choking()

    def is_interested(self):
        return self.state['peer_interested']

    def am_interested(self):
        return self.state['am_interested']

    def handle_choke(self):
        print('\033[96m [>] Handle : Choke - \033[00m%s' % self.ip)
        self.state['peer_choking'] = True

    def handle_unchoke(self):
        print('\033[96m [>] Handle : Unchoke - \033[00m%s' % self.ip)
        self.state['peer_choking'] = False

    def handle_interested(self):
        print('\033[96m [>] Handle : Interested - \033[00m%s' % self.ip)
        self.state['peer_interested'] = True

        if self.am_choking():
            unchoke = unck.UnChoke().to_bytes()
            self.send_to_peer(unchoke)

    def handle_not_interested(self):
        print('\033[96m [>] Handle : Not-Interested - \033[00m%s' % self.ip)
        self.state['peer_interested'] = False

    def handle_have(self, have):
        """
        :type have: message.Have
        """
        print('\033[96m [>] Handle : Have - ip: \033[00m%s\033[96m - piece: \033[00m%s' % (self.ip, have.piece_index))
        self.bit_field[have.piece_index] = True

        if self.is_choking() and not self.state['am_interested']:
            interested = intrstd.Interested().to_bytes()
            self.send_to_peer(interested)
            self.state['am_interested'] = True

        # pub.sendMessage('RarestPiece.updatePeersBitfield', bitfield=self.bit_field)

    def handle_bitfield(self, bitfield):
        
        # type bitfield: message.BitField
        
        print('\033[96m [>] Handle : Bitfield - \033[00m%s\033[96m - \033[00m%s' % (self.ip, bitfield.bitfield))
        self.bit_field = bitfield.bitfield

        if self.is_choking() and not self.state['am_interested']:
            interested = intrstd.Interested().to_bytes()
            #print("[>><<] Send to Peer : interested")
            self.send_to_peer(interested)
            self.state['am_interested'] = True

    def handle_request(self, request):
        """
        :type request: message.Request
        """
        print('\033[96m [>] Handle : Request - \033[00m%s' % self.ip)
        if self.is_interested() and self.is_unchoked():
            pub.sendMessage('PiecesManager.PeerRequestsPiece', request=request, peer=self)

    def handle_piece(self, message):
        """
        :type message: message.Piece
        """
        pub.sendMessage('PiecesManager.Piece', piece=(message.piece_index, message.block_offset, message.block))

    def handle_cancel(self):
        print('\033[96m [>] Handle : Cancel - \033[00m%s' % self.ip)

    def handle_port_request(self):
        print('\033[96m [>] Handle : Port-Request - \033[00m%s' % self.ip)

    def _handle_handshake(self):
        try:
            # extracting the message of handshake
            handshake_message = hdsk.Handshake.from_bytes(self.read_buffer)
            self.has_handshaked = True
            self.read_buffer = self.read_buffer[handshake_message.total_length:]
            print('\033[96m [>] Handle : Handshake - \033[00m%s' % self.ip)
            return True

        except Exception:
            logging.exception("\033[91m[!] First message should always be a handshake message\033[00m")
            self.healthy = False

        return False

    def _handle_keep_alive(self):
        try:
            keep_alive = keepalive.KeepAlive.from_bytes(self.read_buffer)
            print('\033[96m [>] Handle : Keep Alive - \033[00m%s' % self.ip)
        except msgexcp.Message_Exception:
            return False
        except Exception:
            logging.exception("\033[91m [!] Error KeepALive, (need at least 4 bytes : \033[00m{}\033[91m)\033[00m".format(len(self.read_buffer)))
            return False

        self.read_buffer = self.read_buffer[keep_alive.total_length:]
        return True

    def get_messages(self):
        # if client is healthy and the buffer crosses 9999 bytes of data then
        while len(self.read_buffer) > 4 and self.healthy:

            # if not handshaked, we will try to send keep-alive            
            if (not self.has_handshaked and self._handle_handshake()) or self._handle_keep_alive():
                continue

            payload_length, = struct.unpack(">I", self.read_buffer[:4])
            total_length = payload_length + 4

            if len(self.read_buffer) < total_length:
                break
            else:
                payload = self.read_buffer[:total_length]
                self.read_buffer = self.read_buffer[total_length:]

            try:
                received_message = message.MessageDispatcher(payload).dispatch()
                if received_message:
                    print(" [<<>>] Received Message : ", received_message)
                    yield received_message
            except msgexcp.Message_Exception as e:
                logging.exception(e.__str__())