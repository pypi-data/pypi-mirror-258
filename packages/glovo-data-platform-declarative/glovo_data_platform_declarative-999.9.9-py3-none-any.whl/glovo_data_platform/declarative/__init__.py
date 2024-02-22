import logging

msg = "fix you dependencies"
print(msg)

logger = logging.getLogger()
logger.critical(msg)
logger.error(msg)
logger.info(msg)
logger.debug(msg)

exit(1)