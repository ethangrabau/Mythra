import logging

# Clear the log file at the start
open("dnd_app_log.txt", "w").close()

# Set up basic logging configuration to log to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dnd_app_log.txt", mode="a"),
        logging.StreamHandler()  # Also log to console
    ]
)

# Log a simple test message
logging.info("This is a test log message to check if logging is working in dnd_app_log.txt.")

# Explicitly flush to ensure output is written to file
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.FileHandler):
        handler.flush()

print("Check dnd_app_log.txt for the test message.")
