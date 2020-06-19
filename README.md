# wthud
Head-up Display for additional War Thunder data. Written in Python 3.7+, uses data exposed by War Thunder on ```localhost:8111```. The shown data is configurable per aircraft.

Compatible only with Windows! Transparency is handled by the window manager / compositor in most Linux distros, and is therefore neither easy nor portable to handle.

You need a python distribution for Windows, as it is not installed by default. A good choice is e.g. [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Usage
1. Download source code
2. No external libraries needed, just run ```python wthud.py```
3. Start War Thunder, for initial configuration launch a test flight
4. Press on ```Reload```, all variables supported by the current craft will be shown
5. Chose the variables that should be shown in the HUD by checking them. Give names and units in the two checkboxes
6. Save your config with the ```Save``` button.
7. When entering a new game, load a saved config with the ```Load``` button

## License
This program is licensed under a GNU GPL v3 license, see [COPYING](COPYING) for details.
