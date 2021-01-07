__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import message_d.message_exception as msgexcp
from struct import pack, unpack
import message_d.message_exception as msgexcp

class KeepAlive(object):
    #
    #    KEEP_ALIVE = <length>
    #        - payload length = 0 (4 bytes)
    
    payload_length = 0
    total_length = 4

    def __init__(self):
        super(KeepAlive, self).__init__()

    def to_bytes(self):
        return pack(">I", self.payload_length)

    @classmethod
    def from_bytes(cls, payload):
        payload_length = unpack(">I", payload[:cls.total_length])

        if payload_length != 0:
            raise msgexcp.Message_Exception("Not a Keep Alive message")

        return KeepAlive()
