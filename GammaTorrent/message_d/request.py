__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack, unpack
import message_d.message_exception as msgexcp

class Request(object):
    
        # REQUEST = <length><message id><piece index><block offset><block length>
        #     - payload length = 13 (4 bytes)
        #     - message id = 6 (1 byte)
        #     - piece index = zero based piece index (4 bytes)
        #     - block offset = zero based of the requested block (4 bytes)
        #     - block length = length of the requested block (4 bytes)
   
    message_id = 6

    payload_length = 13
    total_length = 4 + payload_length

    def __init__(self, piece_index, block_offset, block_length):
        super(Request, self).__init__()

        self.piece_index = piece_index
        self.block_offset = block_offset
        self.block_length = block_length

    # encoding the data in the given hash format and returning it back
    def to_bytes(self):
        print(" [>><<] Send Request : ",self.payload_length,self.message_id,self.piece_index,self.block_offset,self.block_length)
        return pack(">IBIII",self.payload_length,self.message_id,self.piece_index,self.block_offset,self.block_length)

    @classmethod
    def from_bytes(cls, payload):
        payload_length, message_id, piece_index, block_offset, block_length = unpack(">IBIII",payload[:cls.total_length])
        if message_id != cls.message_id:
            raise msgexp.Message_Exception("Not a Request message")

        return Request(piece_index, block_offset, block_length)