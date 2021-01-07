__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]


from struct import pack, unpack
import random
import socket

class UdpTrackerConnection(object):

    #    connect = <connection_id><action><transaction_id>
    #         connection_id   8-bytes int
    #         action          4-bytes int
    #         transaction_id  4-bytes int
    #
    #    Total length = 8 + 4 + 4 = 16 bytes

    def __init__(self):
        super(UdpTrackerConnection, self).__init__()
        
        # string representation
        # connection_id in unsigned long long int in big endian binary format
        self.conn_id = pack('>Q', 0x41727101980)

        # actions in unsigned int in big endian binary format
        self.action = pack('>I', 0)

        # transaction_id in unsigned int in big endian binary format
        self.trans_id = pack('>I', random.randint(0, 100000))

    def to_bytes(self):
        return self.conn_id + self.action + self.trans_id

    def from_bytes(self, payload):

        # from binary bit string format to respect formats given
        self.action, = unpack('>I', payload[:4])
        self.trans_id, = unpack('>I', payload[4:8])
        self.conn_id, = unpack('>Q', payload[8:])


class UdpTrackerAnnounce(object):
    
        # connect = <connection_id><action><transaction_id>

        # 0-7	    8-byte int	connection_id
        # 8-11	    4-byte int	action	1
        # 12-15 	4-byte int	transaction_id
        # 16-35	    4-byte str	info_hash
        # 36-55    	20-byte str	peer_id
        # 56-63	    8-byte int	downloaded
        # 64-71	    8-byte int	left
        # 72-79	    8-byte int	uploaded
        # 80-83	    4-byte int	event
        # 84-87	    4-byte int	IP address	0
        # 88-91	    4-byte int	key
        # 92-95	    4-byte int	num_want	-1
        # 96-97	    2-byte int	port

        #     - connection_id = 64-bit (8-byte) int
        #     - action = 32-bit (4-byte) int
        #     - transaction_id = 32-bit (4-byte) int

        # Total length = 8 + 4 + 4 = 16 bytes
    

    def __init__(self, info_hash, conn_id, peer_id):
        super(UdpTrackerAnnounce, self).__init__()
        self.peer_id = peer_id
        self.conn_id = conn_id
        self.info_hash = info_hash
        self.trans_id = pack('>I', random.randint(0, 100000))
        self.action = pack('>I', 1)

    def to_bytes(self):
        conn_id = pack('>Q', self.conn_id)
        action = self.action
        trans_id = self.trans_id
        downloaded = pack('>Q', 0)
        left = pack('>Q', 0)
        uploaded = pack('>Q', 0)

        event = pack('>I', 0)
        ip = pack('>I', 0)
        key = pack('>I', 0)
        num_want = pack('>i', -1)
        port = pack('>h', 8000)

        # concatnating the strings
        msg = (conn_id + action + trans_id + self.info_hash + self.peer_id + downloaded + left + uploaded + event + ip + key + num_want + port)

        return msg


class UdpTrackerAnnounceOutput:
    
        # connect = <connection_id><action><transaction_id>

        # 0-3	            32-bit int	action	1
        # 4-7	            32-bit int	transaction_id
        # 8-11	            32-bit int	interval
        # 12-15	            32-bit int	leechers
        # 16-20 	        32-bit int	seeders
        # 20 + 6 * n    	32-bit int	IP address
        # 24 + 6 * n	    16-bit int	TCP port
        # 20 + 6 * N    

    def __init__(self):
        self.action = None
        self.transaction_id = None
        self.interval = None
        self.leechers = None
        self.seeders = None
        self.list_sock_addr = []

    def from_bytes(self, payload):
        self.action, = unpack('>I', payload[:4])
        self.transaction_id, = unpack('>I', payload[4:8])
        self.interval, = unpack('>I', payload[8:12])
        self.leechers, = unpack('>I', payload[12:16])
        self.seeders, = unpack('>I', payload[16:20])
        self.list_sock_addr = self._parse_sock_addr(payload[20:])

    def _parse_sock_addr(self, raw_bytes):
        socks_addr = []

        # socket address : <IP(4 bytes)><Port(2 bytes)>
        # len(socket addr) == 6 bytes

        for i in range(int(len(raw_bytes) / 6)):
            start = i * 6
            end = start + 6
            ip = socket.inet_ntoa(raw_bytes[start:(end - 2)])
            raw_port = raw_bytes[(end - 2):end]
            port = raw_port[1] + raw_port[0] * 256

            socks_addr.append((ip, port))

        return socks_addr
