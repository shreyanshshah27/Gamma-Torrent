__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


import logging
from struct import pack, unpack

# HandShake - String identifier of the protocol for BitTorrent V1
import bitstring

from message_d.choke import Choke
from message_d.request import Request
from message_d.unchoke import UnChoke
from message_d.interested import Interested
from message_d.notinterested import NotInterested
from message_d.have import Have
from message_d.cancel import Cancel
from message_d.bitfield import BitField
from message_d.port import Port
from message_d.piece import Piece
import message_d.message_exception as msgexcp

HANDSHAKE_PSTR_V1 = b"BitTorrent protocol"
HANDSHAKE_PSTR_LEN = len(HANDSHAKE_PSTR_V1)
LENGTH_PREFIX = 4


class MessageDispatcher:

    def __init__(self, payload):
        self.payload = payload

    def dispatch(self):
        try:
            payload_length, message_id, = unpack(">IB", self.payload[:5])
        except Exception as e:
            logging.warning("Error when unpacking message : %s" % e.__str__())
            return None

        map_id_to_message = {
            0: Choke,
            1: UnChoke,
            2: Interested,
            3: NotInterested,
            4: Have,
            5: BitField,
            6: Request,
            7: Piece,
            8: Cancel,
            9: Port
        }

        if message_id not in list(map_id_to_message.keys()):
            raise msgexcp.Message_Exception("Wrong message id")

        return map_id_to_message[message_id].from_bytes(self.payload)


class Message:
    def to_bytes(self):
        raise NotImplementedError()

    @classmethod
    def from_bytes(cls, payload):
        raise NotImplementedError()