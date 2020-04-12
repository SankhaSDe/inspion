__all__ = ['debug','info','warning','error','critical','exception']

import logging
from server.config import *

logging.basicConfig(filename=SERVER_LOG_FILE_NAME,
                    format='%(asctime)s %(message)s',
                    filemode='a') 
logger=logging.getLogger(__name__) 
logger.setLevel(SERVER_LOG_LEVEL) 

def debug(msg):
    logger.debug(msg)
def info(msg):
    logger.info(msg)
def warning(msg):
    logger.warning(msg)
def error(msg):
    logger.error(msg)
def critical(msg):
    logger.critical(msg)
def exception(msg):
    logger.exception(msg)
