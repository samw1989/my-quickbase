import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
print_handler = logging.StreamHandler()
print_handler.setLevel(logging.ERROR)
file_handler = RotatingFileHandler(f'{Path(__file__).resolve().parent}/log.log', maxBytes=20)
file_handler.setLevel(logging.INFO)

p_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
print_handler.setFormatter(p_format)
file_handler.setFormatter(f_format)

logger.addHandler(print_handler)
logger.addHandler(file_handler)

from my_quickbase.quickbase_queries import AppQuery, RecordsQuery
