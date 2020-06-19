# wthud
Head-up Display for additional War Thunder air battle data. Written in Python 3.7+, uses data exposed by War Thunder on ```localhost:8111```. The shown data is configurable per aircraft.

Compatible only with Windows! Transparency is handled by the window manager / compositor in most Linux distros, and is therefore neither easy nor portable to handle.

You need a python distribution for Windows, as it is not installed by default. A good choice is e.g. [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Usage
1. Download source code
2. No external libraries needed, just run ```python wthud.py```
3. War Thunder needs to be in borderless or windowed mode, fullscreen won't show the overlay
4. Start War Thunder, for initial configuration launch a test flight
5. Press on ```Reload```, all variables supported by the current craft will be shown
6. Chose the variables that should be shown in the HUD by checking them. Give names and units in the two checkboxes
7. Save your config with the ```Save``` button.
8. When entering a new game, load a saved config with the ```Load``` button

## Implementation Details
War Thunder exposes craft telemetry data on a web interface at ```localhost:8111``` during air battles. This data can be looked at on a second screen in a quite awkward GUI. This project aims to make the presented information more useful by overlaying select telemetry data directly on the game window, similarly to the already present (but limited) data.

Data is collected from the in-game webserver using the ```requests``` library and displayed on screen with a transparent, undecorated Tk window. The data to be shown can be configured individually per aircraft, and is saved between sessions in json files residing inside the [configs](configs) folder.

## Usage Disclaimer
This tool is neither sponsored, endorsed or otherwise approved by Gaijin Entertainment. It merely presents readily available data in a comfortable manner. Use at your own risk, at the time of writing similar tools were more or less "tolerated" when asked about on Gaijin's forums. No liability will be held by the authors should this and similar tools be the reason for the ban or termination of your War Thunder account.

## Contributions
Pull Requests and issues are welcome, expect a slow response as this project is developed in the free time of volunteers.

## TODO / Future Features
- [ ] Change order of shown items
- [ ] Position shown items individually
- [ ] Logging
- [ ] Better UI framework, possibly Qt
- [ ] General UI cleanup (WIP)
- [ ] Code cleanup / documentation (WIP)
- [ ] Cross-platform support (possibly impossible)
- [ ] Extension interface for calculated telemetry data (WIP)

## License
This program is licensed under a GNU GPL v3 license, see [COPYING](COPYING) for details.
