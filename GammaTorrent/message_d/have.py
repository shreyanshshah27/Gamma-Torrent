__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack , unpack
import message_d.message_exception as msgexcp

class Have(object):
    
        # HAVE = <length><message_id><piece_index>
        #     - payload length = 5 (4 bytes)
        #     - message_id = 4 (1 byte)
        #     - piece_index = zero based index of the piece (4 bytes)
    
    message_id = 4

    payload_length = 5
    total_length = 4 + payload_length

    def __init__(self, piece_index):
        super(Have, self).__init__()
        self.piece_index = piece_index

    def to_bytes(self):
        pack(">IBI", self.payload_length, self.message_id, self.piece_index)

    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id, piece_index = unpack(">IBI", payload[:cls.total_length])
        if message_id != cls.message_id:
            raise msgexcp.Message_Exception("Not a Have message")

        return Have(piece_index)