import logging
from datetime import date

current_date = date.today()

logger = logging
logger.basicConfig(filename=f"logging\{current_date}.log", level=logging.INFO,
                        filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
