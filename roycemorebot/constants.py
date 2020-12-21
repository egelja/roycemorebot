import logging
import os

log = logging.getLogger(__name__)

TOKEN = os.environ["BOT_TOKEN"]

DEBUG_MODE = True if os.environ["DEBUG"] is not None else False
