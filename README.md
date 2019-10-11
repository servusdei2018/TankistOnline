# TankistOnline
A Cross-Platform Lightweight 2D Tank Multiplayer Game in Python. **Note that this is a work-in-progress**, and is not yet complete or playable.

![Build #13 Screenshot](https://github.com/servusDei2018/servusdei2018.github.io/blob/TankistOnline/Tankist_Screenshot.png?raw=true)

## Running

Current development is focused around `TankistOnlie_Client.py` and `TankClass.py`.

To run the (mock) client, `python TankistOnline_Client.py` or `python3 TankistOnline_Client.py`

## Dependencies

- **Pyglet**
- (Optional) **VLC-Python** bindings [Necessary for Sound Effects, Requires VLC Media Player to be installed.]

## To-Do:

### Server-Side:
- [X] ~~Create the server. Because this is lightweight, it has to be single-threaded.~~
- [X] ~~Add a HP and a death system to the server.~~

### Client-Side:
- [X] ~~Create relative XY values for each Tank, in TankClass. This shall allow the viewport to move, to allow maps bigger~~
      than the window size.
- [X] ~~Update the screen even if the `on_draw()` event wasn't called.~~
- [X] ~~Ensure that the theme is looped, currently when the track ends, it doesn't replay it.~~
- [ ] Make possible a scrollable terrain-background.
- [ ] Update the client to work with the server.

### Misc:

- [ ] Document code more clearly
- [ ] Optimization [it's always welcome, however, keep in mind our Cross-Platform mindset]
- [X] ~~Creating and maintaining the [Wiki](https://github.com/servusDei2018/TankMMO/wiki)~~
- [ ] Make the [Wiki](https://github.com/servusDei2018/TankMMO/wiki) more concise.

## Contributing

Feel free to fork the project, and push contributions to the *beta* branch, **unless otherwise directed** by a help-wanted post in Issues.

## License

This project is released under the GPLv3.0.

It permits the Commercial and Private Use and Modification, Distribution, and Patent Priviledges. However, the Conditions are you disclose the source code, use the **same license**, include both the license and copyright notice, and state changes. 

*Disclaimer: This summary of the License in no way claims to be the authoratative license to which those who use this project are bound*
