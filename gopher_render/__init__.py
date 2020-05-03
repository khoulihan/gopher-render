from ._parser import GopherHTMLParser
# This is to allow poetry to run the main function
# as a script. Not ideal really
# TODO: Figure out a better way to run the module during development.
from .__main__ import main
