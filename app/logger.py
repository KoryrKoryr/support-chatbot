import logging
from logging.handlers import TimedRotatingFileHandler
import os
from colorama import Fore, Style, init

# Initialize colorama (for Windows + cross-platform color)
init(autoreset=True)

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Define a custom formatter
class CustomFormatter(logging.Formatter):
    """Add colors to log levels for terminal output."""
    
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        formatted = f"{Style.BRIGHT}{log_color}{record.levelname:<8}{Style.RESET_ALL} {record.getMessage()}"
        return f"{record.asctime} | {formatted}"
    
# Configure file handler (rotating daily)
file_handler = TimedRotatingFileHandler(
    filename="logs/app.log",
    when="midnight",      # rotate logs every midnight
    interval=1,           # every 1 day
    backupCount=7,        # keep 7 days of logs
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

# Configure console handler (colorized)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter("%(asctime)s"))

# Final logger setup
logger = logging.getLogger("support-chatbot")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
