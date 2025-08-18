# MITRE ATT&CK® Matrix for Enterprise - Anki Decks (work in progress)

Anki decks for the tactics, techniques, and subtechniques covered in the MITRE ATT&CK® Enterprise Matrix built from components in the MITRE cti github repository [linked here](https://github.com/mitre/cti)

Loosely adapted from MITRE ATT&CK® related python code covered in Anthony Isherwood's Detection Engineering focused course 
* GitHub repo for code covered in their detection engineering course [here](https://github.com/isherwood-sec/detection-engineering)
* TCM Academy "Detection Engineering for Beginners" version listed on their site [here](https://aisherwood.me/courses/)
* Newer course site for "Detection Engineering 101: Start Your Journey" [here](https://www.isherwoodsec.com/)

## Requirements

Building the decks from the python scripts requires the genanki library and Python 3+

The genanki library can be installed using "pip install genanki"

* Genanki PyPI listing - <https://pypi.org/project/genanki/>
* Genanki repo - <https://github.com/kerrickstaley/genanki>

## Building decks

To build decks via the python scripts, simply run it in a python3 environment

E.g., "python3 tactic\_deck\_builder.py" to build the deck covering tactics

The python scripts can be customized to have card types, font, etc. changed; refer to genanki documentation from genanki repo above for more information on note, note models, and deck creation
