__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack, unpack
import message_d.message_exception as msgexcp

class Port(object):
    
        # PORT = <length><message id><port number>
        #     - length = 5 (4 bytes)
        #     - message id = 9 (1 byte)
        #     - port number = listen_port (4 bytes)
    
    message_id = 9

    payload_length = 5
    total_length = 4 + payload_length

    def __init__(self, listen_port):
        super(Port, self).__init__()

        self.listen_port = listen_port

    def to_bytes(self):
        return pack(">IBI",self.payload_length,self.message_id,self.listen_port)

    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id, listen_port = unpack(">IBI", payload[:cls.total_length])

        if message_id != cls.message_id:
            raise msgexcp.Message_Exception("Not a Port message")

        return Port(listen_port)
