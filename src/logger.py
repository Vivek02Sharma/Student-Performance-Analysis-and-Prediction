import logging
import os
from datetime import datetime

# Define log directory and create it if it doesn't exist
log_directory = os.path.join(os.getcwd(), "logs")
os.makedirs(log_directory, exist_ok=True)

# Generate a timestamped log file name
timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
log_filename = f"log_{timestamp}.log"
log_filepath = os.path.join(log_directory, log_filename)

# Set up the logging configuration
logging.basicConfig(
    filename=log_filepath,
    format="[%(asctime)s] %(filename)s:%(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

