# TurnipMaster
Never dreamed of being a bellionaire in Animal Crossing New Horizons?

TurnipMaster is a command-line application that help you find the perfect island for buying and selling turnips.

Just type your username, and let the application do the rest!it st

## Installation

- Install `firefox` and add `geckodriver` to your system path
- Install `python3.7` or higher
- Install `pip3`
- Install virtualenv via pip3
    - `pip3 install virtualenv`
- Create a virtual environment called `venv`
    - `virtualenv venv`
- Activate the virtualenv: 
    - macOS/Linux 
        - `source venv/bin/activate`
    - Windows
        - `\venv\Scripts\activate.bat`
- Once the virtualenv is activated, install the required dependencies inside it
    - `pip3 install -r requirements.txt`

## Usage

Simply run the application with python3

    python3 turnipexchange.py --name Username

You can check for additional parameters via `--help` (*HIGHLY RECOMMENDED*)

    python3 turnipexchange.py --help

### License

This software is licensed under MIT License. See LICENSE file for more information.
