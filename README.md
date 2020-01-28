# Laboratoire de Talos - PyBot

This is the python bot for the Discord server "Le Laboratoire de Talos", a french community about philosophy and science.

Public link, feel free to share: https://discord.gg/fkGsYDd


## Terms of this repository

This repository is made public so that any bug, safety breach or improvement opportunity can be detected by our community.

If you find something worth a look, please send a private message to Weazel on the above Discord server.

It is possible to contribute via a clone of this repository and a pull-request. If you are really motivated, you can also offer to join us on the coding team (which is only one person for now, and not very active).


## Installing the project

Python 3.6.x or **earlier** is required, because Python 3.7.x and later introduce backward compatibility issues with discord API.

Create a virtual environment with Python 3.6.10 for example and install ```discord.py``` in it.

Clone the repository and select the virtual environment as the project interpreter with your favorite IDE.


## Architecture

It is a very simple bot whose functionnalities are limited to: simple commands, charter acceptance, funny commands, voice-text channel link.

The main file is bot.py, which is responsible for initialization and handling the different discord events.

utils.py introduces a bunch of useful functions and litterals specific to our discord server. It also contains the list of commands.

The directory commands contains a the parent class Command and its different inherited classes, one for each command the bot can execute.


## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details
