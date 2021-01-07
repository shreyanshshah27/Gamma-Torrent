__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import logging
import os
import time

import tracker_d.tracker as tck
from block import State

import peers_d.peers_manager as pem
import pieces_d.pieces_manager as pim
import message_d.message as msg
import message_d.request as req
import torrents_d.torrent as tor


class MainManager(object):
    last_progress = -1
    last_log_line1 = ""
    last_log_line2 = ""

    # constructor for initializing variables with the respective values from the torrent file entered
    def __init__(self, torrent_file_name):

        # getting content of the torrent file
        self.torrent = tor.Torrent().load_content(os.path.join("torrents_d","sample_torrents",str(torrent_file_name)))
        logging.info("[+] Content of the Torrent file Loaded..")

        # creating a tracker
        self.tracker = tck.Tracker(self.torrent)

        # creating a manager for pieces
        self.pieces_manager = pim.PiecesManager(self.torrent)

        # creating a manager for peers
        self.peers_manager = pem.PeersManager(self.torrent, self.pieces_manager)

        self.peers_manager.start()

        logging.info("[+] Manager for Peers Started")
        logging.info("[+] Manager for Pieces Started")

    def start(self):
        # scrapping data from trackers
        peers_dict = self.tracker.get_peers_from_trackers()

        # adding peers to the list who have completed handshake
        self.peers_manager.add_peers(peers_dict.values())

        # Looping until all the pieces are completed
        while not self.pieces_manager.all_pieces_completed():

            # if we dont have any unchocked peers, then try again
            if not self.peers_manager.has_unchoked_peers():
                time.sleep(1)
                print("\033[92m [!] No unchocked peers\033[00m")
                continue

            # else if we have any unchocked peers then   
            for piece in self.pieces_manager.pieces:
                index = piece.piece_index

                # if the piece is full then skip to next piece
                if self.pieces_manager.pieces[index].is_full:
                    continue
                
                # select any random peer from the list who meets the conditions
                peer = self.peers_manager.get_random_peer_having_piece(index)
                if not peer:
                    continue

                # if the block is pending for too long, then we will free that block
                self.pieces_manager.pieces[index].update_block_status()

                data = self.pieces_manager.pieces[index].get_empty_block()
                if not data:
                    continue

                piece_index, block_offset, block_length = data
                
                # getting the different fields into a unified encoded format for a request.
                piece_data = req.Request(piece_index, block_offset, block_length).to_bytes()
                peer.send_to_peer(piece_data)

            self.display_status()

            time.sleep(0.1)

        print("[+] File(s) downloaded successfully.")
        self.display_status()

        self._exit_threads()

    # display the log of current status of downloading
    def display_status(self):
        progress = 0

        # Calculating the Progress of the data downloaded after each block of all pieces is completely full
        for i in range(self.pieces_manager.number_of_pieces):
            for j in range(self.pieces_manager.pieces[i].number_of_blocks):
                if self.pieces_manager.pieces[i].blocks[j].state == State.FULL:
                    progress += len(self.pieces_manager.pieces[i].blocks[j].data)


        if progress == self.last_progress:
            return

        number_of_peers = self.peers_manager.unchoked_peers_count()
        percentage_completed = float((float(progress) / self.torrent.total_length) * 100)

        current_log_line1 = "\033[92m [+] Connected peers: \033[00m{}".format(number_of_peers)
        current_log_line2 = "\033[95m [+] \033[00m{}% \033[95mcompleted - \033[00m{}/{} \033[95mpieces\033[00m".format(round(percentage_completed, 2),self.pieces_manager.complete_pieces,self.pieces_manager.number_of_pieces)
        
        # displays the number of seeders whenever the number changes
        if current_log_line1 != self.last_log_line1:
            print(current_log_line1)

        # Dislaying the unique log line ie. after some considerable percentage is downloaded.
        if current_log_line2 != self.last_log_line2:
            print(current_log_line2)

        self.last_log_line1 = current_log_line1
        self.last_log_line2 = current_log_line2
        self.last_progress = progress

    def _exit_threads(self):
        self.peers_manager.is_active = False
        os._exit(0)