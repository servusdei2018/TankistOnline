# TankistOnline
A Cross-Platform Lightweight 2D Tank Multiplayer Game in Python 2/3.

### Commitments:

**Tiny System Requirements** -- A Raspberry Pi can run a server and 4 clients, with room to spare. The RPi is a 1Ghz quad core processor with 1 GB of RAM.

**Tiny Size** -- v0.1:Alpha is < 137 KB (unzipped)

**Cross-Platform** -- Windows, Mac, Linux; anything that runs Python.

![Build #52 Screenshot](https://github.com/servusDei2018/servusdei2018.github.io/blob/master/screenShots/connecting.jpg?raw=true)
![Build #52 Screenshot](https://github.com/servusDei2018/servusdei2018.github.io/blob/master/screenShots/gameplay.jpg?raw=true)

## UPDATES

### Version 0.1 Alpha Released!

**Version 0.1 Alpha is now available!** If you experience any bugs or have any questions, please
feel free to open a new issue. V0.1:Alpha features:

```
-Interactive multiplayer client-server gameplay, with nicknames for each player
-Shooting other tanks (and killing them)
-Driving across the map (with map boundaries to prevent people from driving infinitessimal distances)
-A colored life-bar
-The server automatically disconnects idle players
-**Client is Python 3 ONLY**
-**Server is Python 2.7+, Python 3.x, or PyPy**
```

Special thanks to all of our contributors and everyone who is helping with this project!

Please note that **we are looking for someone to host a public server, to which anyone can connect.** 
To host Tankist, you can either pay for a 24/7 VPS (which costs from $2-8/mo.) or you may just decide to
run Tankist on your own computer at a specified time each day/week/month -- and that information shall be
made available via this repository. If you have any questions about hosting Tankist, need help choosing or
setting up a VPS, or questions about sponsoring a Server, please open a new issue.

### Upcoming: Version 0.12 Alpha

Version 0.12 Alpha should be released by December 13th and feature a scrolling background.

### Upcoming: Version 0.2 Alpha

Version 0.2 Alpha should be available as soon as mid-December, but definitely by the end of January, 2020. It shall feature:

```
-More and improved code optimization
-A scrolling background
-Cleaner, more concise code
-A new and improved wiki
-A lobby for people to connect to public hosts
-Notifies players if they chose a nickname already taken
```

And things that __may__ make an appearance in *future* releases:

```
-Different TURRETS that do different amounts of damages from different ranges
-Tank skins to customize the look and feel
-Capture the flag mode
-Deathmatch mode
-Team deathmatch mode
```

### Changelog:

The project was last updated on `November 20, 2019` with many additions to both the client and the server.

```
Changelog:

-Server improved
-Client improved
```

## RUNNING

**The Client is Python 3 _only_, whereas the server can be run with Python 2.7+, Python 3.x, or PyPy**

### Running the client

If you don't have it, install pyglet: `pip3 install pyglet`
To run the client, **Python 3 must be used:** `python3 TankistOnline_Client.py`

Before you'll be able to play, you'll have to run the server (see below).

Once the client is running, you'll be asked to enter a nickname, then you'll connect
and be able to move around (arrow keys) and shoot (spacebar). If you want a landmark
by which to mark your movements, connect with another client. You may need to move
around a bit before your tanks are able to see each other.

### Running the server

For ease of deployment on varied systems, the server can be run with `python2.7+`, `python3.x`, and `PyPy`. The speed
difference between the interpreters is not significant, but will affect CPU usage and RAM (around 6-10%).

PyPy (fastest): `pypy TankistOnline_Server.py`
Python3.x: `python3 TankistOnline_Server.py`
Python2.7+ (slowest): `python TankistOnline_Server.py`

### Playing the game

**The client screen centers on the player's tank,** so it won't look like your tank is moving. If someone else joins the server, you'll be able to use him as a landmark.

## DEPENDENCIES

To keep to our lightweight commitment, dependencies for the client are minimal, and the server *has no dependencies* beyond the standard library.

### Client side dependencies:

- **Pyglet** (`pip install pyglet`, *or* `pip3 install pyglet`)

### Server side dependencies:

- **None**

## TO-DO:

### Server-Side:
Pending

### Client-Side:
Pending

### Misc:
- [ ] Optimization [it's always welcome, however, keep in mind our Cross-Platform mindset].
- [ ] Maintain the Wiki to reflect the contents of the `doc` folder. {`WIKI`}

## CONTRIBUTING

Feel free to fork the project, and push contributions to the *beta* branch, unless otherwise directed by a Help Wanted topic in Issues.

## LICENSE

Copyright (C) 2019. All Rights Reserved.

This project is released under the GPLv3.0.

It permits the **Commercial and Private Use and Modification, Distribution, and Patent Priviledges.** However, the Conditions are that you must **disclose the source code**, use the **same license**, **include both the license and copyright notice**, and **state changes**. 

*Disclaimer: **This summary of the License is not the license itself**.*
