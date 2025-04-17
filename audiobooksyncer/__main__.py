from loguru import logger

from .scripts.cli import main

logger.remove()  # remove default logger

logger.add(
    'app.log',
    level='DEBUG',
    format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
)

main()
