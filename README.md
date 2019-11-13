# TankistOnline
A Cross-Platform Lightweight 2D Tank Multiplayer Game in Python. **Note that this is a work-in-progress**, and is not yet complete or playable.

![Build #13 Screenshot](https://github.com/servusDei2018/servusdei2018.github.io/blob/TankistOnline/Tankist_Screenshot.png?raw=true)

## Updates

With hope (and a lot of hard work), **version 0.1 Alpha shall be released this December 1st**! It shall feature:

```
-Interactive multiplayer client-server gameplay, with nicknames for each player that appear above each tank
-Shooting other tanks (and killing them)
-Driving across the map (with map boundaries to prevent people from driving infinitessimal distances)
-Python 2/3 support
```

and if things go better than expected, it may feature any of the following:

```
-Sound (without the need for VLC Media Player)
-A client-side HUD (heads-up-display)
```

Once again, special thanks to all our contributors and everyone who is helping with this project!

### Changelog:

The project was last updated on `November 8, 2019` with the re-writing of the Server and large modification of the Client.

```
Changelog:

-Server re-written
-Client overhauled
-Directory structure re-framed
-Documentation folder 'doc' added
```

## Running

**TankistOnline should work with both Python 3.x and Python 2.7+**, however we reccomend Python 3.

To run the (mock) client, `python TankistOnline_Client.py` or `python3 TankistOnline_Client.py`

## Dependencies

- **Pyglet** (`pip install pyglet`, *or* `pip3 install pyglet`)

## To-Do:

### Server-Side:
- [X] ~~Create the server. Because this is lightweight, it has to be single-threaded.~~
- [X] ~~Add a HP and a death system to the server.~~
- [X] ~~Rewrite the server to use UDP.~~
- [ ] When the client is finished, bugtest the server.

### Client-Side:
- [X] ~~Create relative XY values for each Tank, in TankClass. This shall allow the viewport to move, to allow maps bigger~~
      than the window size.
- [X] ~~Update the screen even if the `on_draw()` event wasn't called.~~
- [ ] Make the client interact with the server. {`NETWORKING`}
- [ ] Make possible a scrollable terrain-background. {`GRAPHICS`}

### Misc:

- [X] ~~Create the Wiki~~
- [ ] Document code more clearly. {`WIKI`}
- [ ] Optimization [it's always welcome, however, keep in mind our Cross-Platform mindset].
- [ ] Maintain the Wiki to reflect the contents of the `doc` folder. {`WIKI`}

## Contributing

**Note that some parts of the Client are going to undergo significant change when it is updated to interact with the server.**

Feel free to fork the project, and push contributions to the *beta* branch, unless otherwise directed by a Help Wanted topic in Issues.

## License

This project is released under the GPLv3.0.

It permits the Commercial and Private Use and Modification, Distribution, and Patent Priviledges. However, the Conditions are you **disclose the source code**, use the **same license**, **include both the license and copyright notice**, and **state changes**. 

*Disclaimer: **This summary of the License is not the license itself**.*
