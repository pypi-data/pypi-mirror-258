import logging

msg = "fix your dependencies"
print(msg)

logger = logging.getLogger()
logger.critical(msg)
logger.error(msg)
logger.info(msg)
logger.debug(msg)

exit(1)