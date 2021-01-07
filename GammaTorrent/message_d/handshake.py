__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack, unpack
import message_d.message_exception as msgexcp

HANDSHAKE_PSTR_V1 = b"BitTorrent protocol"
HANDSHAKE_PSTR_LEN = len(HANDSHAKE_PSTR_V1)
LENGTH_PREFIX = 4

class Handshake(object):
    
    
        # Handshake = <pstrlen><pstr><reserved><info_hash><peer_id>
        #     - pstrlen = length of pstr (1 byte)
        #     - pstr = string identifier of the protocol: "BitTorrent protocol" (19 bytes)
        #     - reserved = 8 reserved bytes indicating extensions to the protocol (8 bytes)
        #     - info_hash = hash of the value of the 'info' key of the torrent file (20 bytes)
        #     - peer_id = unique identifier of the Peer (20 bytes)

        # Total length = payload length = 49 + len(pstr) = 68 bytes (for BitTorrent v1)
    
    payload_length = 68
    total_length = payload_length

    def __init__(self, info_hash, peer_id=b'-ZZ0007-000000000000'):
        super(Handshake, self).__init__()

        assert len(info_hash) == 20
        #assert legood guessn(peer_id) < 255
        self.peer_id = peer_id
        self.info_hash = info_hash

    # creating an encoded string of data for the handshake
    def to_bytes(self):
        reserved = b'\x00' * 8
        handshake = pack(">B{}s8s20s20s".format(HANDSHAKE_PSTR_LEN),HANDSHAKE_PSTR_LEN,HANDSHAKE_PSTR_V1,reserved,self.info_hash,self.peer_id)

        return handshake

    @classmethod
    def from_bytes(cls, payload):
        pstrlen, = unpack(">B", payload[:1])
        pstr, reserved, info_hash, peer_id = unpack(">{}s8s20s20s".format(pstrlen), payload[1:cls.total_length])

        if pstr != HANDSHAKE_PSTR_V1:
            raise ValueError("Invalid string identifier of the protocol")

        return Handshake(info_hash, peer_id)