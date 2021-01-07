__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack, unpack
import message_d.message_exception as msgexcp

class Choke(object):

        # CHOKE = <length><message_id>
        #     - payload length = 1 (4 bytes)
        #     - message id = 0 (1 byte)
    
    message_id = 0
    chokes_me = True

    payload_length = 1
    total_length = 5

    def __init__(self):
        super(Choke, self).__init__()

    def to_bytes(self):
        return pack(">IB", self.payload_length, self.message_id)

    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id = unpack(">IB", payload[:cls.total_length])
        if message_id != cls.message_id:
            raise msgexp.Message_Exception("Not a Choke message")

        return Choke()
