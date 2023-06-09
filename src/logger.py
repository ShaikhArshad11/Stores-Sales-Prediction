import logging
from datetime import datetime
import os

#Declaring log variables
LOG_DIR="sales_logs"
CURRENT_TIME_STAMPS= f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_FILE_NAME= f"log_{CURRENT_TIME_STAMPS}.log"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH= os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode='w',
                    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )