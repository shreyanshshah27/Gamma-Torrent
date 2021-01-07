__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import math
import hashlib
import time
from bcoding import bencode, bdecode
import logging
import os


class Torrent(object):

    # initializing variables using constructor
    def __init__(self):
        self.torrent_file = {}
        self.total_length: int = 0
        self.piece_length: int = 0
        self.pieces: int = 0
        self.info_hash: str = ''
        self.peer_id: str = ''
        self.announce_list = ''
        self.file_names = []
        self.number_of_pieces: int = 0

    # a function to create the similar directory structure as directed in the torrent file
    def init_files(self):
        # getting file name or folder name
        root = self.torrent_file['info']['name']

        # Case : directory
        # files keyword is when the torrent has a directory to download
        if 'files' in self.torrent_file['info']:
            
            # checking piece_indexif the folder exists or not : if not, creating the directory
            if not os.path.exists(root):
                os.mkdir(root, 0o0766 )
            
            # creating 
            for file in self.torrent_file['info']['files']:
                path_file = os.path.join(root, *file["path"])

                if not os.path.exists(os.path.dirname(path_file)):
                    os.makedirs(os.path.dirname(path_file))

                # adding file_path and its length to the dictionary
                self.file_names.append({"path": path_file , "length": file["length"]})
                
                # calculating the total size of folder
                self.total_length += file["length"]
        
        # Case : file
        else:
            self.file_names.append({"path": root , "length": self.torrent_file['info']['length']})
            self.total_length = self.torrent_file['info']['length']

    # a function to get the url list of the tracker
    def get_trackers(self):
        if 'announce-list' in self.torrent_file:
            return self.torrent_file['announce-list']
        else:
            return [[self.torrent_file['announce']]]

    # a function to generate a 20 byte SHA1 hash peer_id
    def generate_peer_id(self):
        seed = str(time.time())
        return hashlib.sha1(seed.encode('utf-8')).digest()

    # a function to load the content of the torrent files
    def load_content(self, path):
        with open(path, 'rb') as file:
            contents = bdecode(file)

        self.torrent_file = contents

        # getting metainfo of torrent file in separate variables
        """
            Please refer to https://en.wikipedia.org/wiki/Torrent_file#File_structure 
            for understanding the structure of Torrent files containing metainfo
        """
        
        # creating hash info for handshaking purpose
        raw_info_hash = bencode(self.torrent_file['info'])
        self.info_hash = hashlib.sha1(raw_info_hash).digest()
        self.peer_id = self.generate_peer_id()

        # creating directory structure and store file info in the dictionary
        self.announce_list = self.get_trackers()
        self.init_files()

        # creating number of pieces
        self.piece_length = self.torrent_file['info']['piece length']
        self.pieces = self.torrent_file['info']['pieces']
        self.number_of_pieces = math.ceil(self.total_length / self.piece_length)

        # checking for the lengths.. if equal to zero, it will show an assertion error
        assert(self.total_length > 0)
        assert(len(self.file_names) > 0)

        # return all the values
        return self
