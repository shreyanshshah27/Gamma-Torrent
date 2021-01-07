# Gamma-Torrent (γ-Torrent)
Simple Implementation of BitTorrent-Client in Python

## Table of content

- [what is γ-Torrent?](#description)
- [Features](#features)
- [How to Install γ-Torrent?](#installation)
- [How to run γ-Torrent?](#configure)
- [Dependencies](#list-of-dependencies)
- [Screenshots](#screenshots)
- [Support](#support)

### Description

Gamma-Torrent (γ-Torrent) is a basic Python based BitTorrent-Client tool which can be accessed using Command-Line-Interface. It was created as an end semester collaborative project for Computer Networks course. The main motive of this project was to implement simple Bittorrent-Client adn add few innovative ideas to improve the performance of GammaTorrent. 


### Features

Until now, only few features have been completed, rather are yet to implement
- [X] HTTP scraper
- [X] UDP scraper
- [X] Connecting peers and Handshaking
- [X] BitTorrent Peer to Tracker Communication
- [X] Rarest Piece First Algo *(Yet left to intergrate it)*
- [X] Can download multiple files from a single torrent
- [ ] Cannot Run with multiple torrent files a time. *(Ofcourse you can use multiple terminals and download content using torrents individually)*
- [ ] Pause / Resume Functionality is missing yet
- [ ] Adding more algos like End-Game Algo, Super Seeding Algo, Tit-for-Tat Algo (Choking Algo), etc. for making GammaTorrent more efficient
- [ ] Downloading and Uploading speeds

### Installation

- Clone the repo using :
> $ git clone https://github.com/caped-crusader16/Gamma-Torrent.git
<br/>

- After complete cloning, enter directory GammaTorrent under Gamma-Torrent-master directory
> $ cd Gamma-Torrent-master/GammaTorrent
<br />

### Configure

- To install the dependencies by itself
>	$ pip install -r requirements.txt

- To run the project
>	$ python3 main.py react.torrent

**Format :**  <br />
> 	$ python3 main.py <torrent_file_name>

**Note :** This torrent file should be present in the *'torrent_d/sample_torrents'* directory to run. You just need to include the file name in the command where the torrent should exist in the directory mentions. Currently, only *'react.torrent'* file is present in the given directory


### List of Dependencies

> bcoding==1.5 <br />
> bitstring == 3.1.7 <br />
> PyPubSub == 4.0.3 <br />
> requests >= 2.24.0 <br />
> pubsub == 0.1.2 <br />
> ipaddress == 1.0.23 <br />

### ScreenShots

- **Image-1 :** Starting of Torrent; Connecting with the peers <br />

![Image 1](https://github.com/caped-crusader16/Gamma-Torrent/blob/main/images/img1.png)
<br /> <br />
- **Image-2 :** Connecting with peers using Sockets; Handling Handshakes with the connected peers <br />

![Image 2](https://github.com/caped-crusader16/Gamma-Torrent/blob/main/images/img2.png)
<br /> <br />
- **Image-3 :** Handling Handshakes and BitFields with the peers <br />

![Image 3](https://github.com/caped-crusader16/Gamma-Torrent/blob/main/images/img3.png)
<br /> <br />
- **Image-4 :** Handling choke, unchoke peers; Downloading content in pieces <br />

![Image 4](https://github.com/caped-crusader16/Gamma-Torrent/blob/main/images/img4.png)

### References
- [BitTorrent Specifications](https://wiki.theory.org/BitTorrentSpecification#Peer_wire_protocol_.28TCP.29)
- [BitTorrent Official Web.](https://www.bittorrent.org/beps/bep_0003.html)
- [Allen Kim's Blog](http://allenkim67.github.io/programming/2016/05/04/how-to-make-your-own-bittorrent-client.html)
- [Kristen Widman's Blog](http://www.kristenwidman.com/blog/how-to-write-a-bittorrent-client-part-1)
- [Reference Article-1](https://www.researchgate.net/publication/223808116_Implementation_and_analysis_of_the_BitTorrent_protocol_with_a_multi-agent_model)
- [Reference Article-2](http://dandylife.net/docs/BitTorrent-Protocol.pdf)
- [Reference Article-3](http://web.cs.ucla.edu/classes/cs217/05BitTorrent.pdf)

## Authors

[**Manav Vagrecha**](https://github.com/caped-crusader16) , [**Devam Shah**](https://github.com/Devam911) , [**Shreyansh Shah**](https://github.com/shreyanshshah27)

### Support

- If you really like the project then please give us a star :star:
- If you are interested to add some new features or make any improvements, ping me up at [Email](manavvagrecha1321@gmail.com) with a detailed explanation of your approach **OR** send a pull request **OR** File an issue with detailed description.
