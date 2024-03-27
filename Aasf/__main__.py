import logging
import importlib
from pyrogram import *

from Aasf import *
from Aasf.plugins import *

FORMAT = "%(message)s"

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
    )
    for module in ALL_MODULES:
      importlib.import_module("Aasf.plugins." + module)
    logging.getLogger("pyrogram").setLevel(logging.INFO)    
    idle()
