import os

from loguru import logger

from .scripts.cli import main

logger.remove()  # remove default logger

logger.add(
    'app.log',
    level=os.getenv('LOGGING_LEVEL', 'DEBUG'),
    format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
)

main()
