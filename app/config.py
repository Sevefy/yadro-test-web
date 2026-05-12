import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# we need addHandler to combine handler with logger
logger.addHandler(console_handler)

#### formatter ####
formatter = logging.Formatter(
    "%(levelname)s: %(asctime)s %(message)s"
 )
# we need setFormatter to combine handler with handler
console_handler.setFormatter(formatter)