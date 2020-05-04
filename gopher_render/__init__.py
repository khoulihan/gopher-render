from ._parser import GopherHTMLParser
# This is to allow poetry to run the main function
# as a script. Not ideal really
# TODO: It is unclear why, but running the script using the entrypoint
# specified in the setup.py relies on main being imported here.
from .cli import main
