__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack , unpack
import message_d.message_exception as msgexcp

class Piece(object):
    
        # PIECE = <length><message id><piece index><block offset><block>
        # - length = 9 + block length (4 bytes)
        # - message id = 7 (1 byte)
        # - piece index =  zero based piece index (4 bytes)
        # - block offset = zero based of the requested block (4 bytes)
        # - block = block as a bytestring or bytearray (block_length bytes)

    message_id = 7

    payload_length = -1
    total_length = -1

    def __init__(self, block_length, piece_index, block_offset, block):
        super(Piece, self).__init__()

        self.block_length = block_length
        self.piece_index = piece_index
        self.block_offset = block_offset
        self.block = block

        self.payload_length = 9 + block_length
        self.total_length = 4 + self.payload_length

    def to_bytes(self):
        return pack(">IBII{}s".format(self.block_length),self.payload_length,self.message_id,self.piece_index,self.block_offset,self.block)

    @classmethod
    def from_bytes(cls, payload):
        block_length = len(payload) - 13
        payload_length, message_id, piece_index, block_offset, block = unpack(">IBII{}s".format(block_length),payload[:13 + block_length])

        if message_id != cls.message_id:
            raise msgexcp.Message_Exception("Not a Piece message")

        return Piece(block_length, piece_index, block_offset, block)
