__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

import logging
import sys
import main_manager

if __name__ == '__main__':
    # configuring the log outputs to the debug level
    logging.basicConfig(level=logging.DEBUG)

    torrent_name = str(sys.argv[1])

    # runs the constructor and gets the file content
    mngr = main_manager.MainManager(torrent_name)
    mngr.start()