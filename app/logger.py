import logging
from logging.handlers import TimedRotatingFileHandler
import os
from colorama import Fore, Style, init

# --- Initialize colorama for cross-platform color output ---
init(autoreset=True)

# --- Ensure logs directory exists ---
os.makedirs("logs", exist_ok=True)

# ============================================================
# Custom Formatter for Console Output
# ============================================================
class CustomFormatter(logging.Formatter):
    """Adds colors and timestamps to console log messages."""

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record):
        # Color by level
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        # Proper timestamp
        time_str = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        # Pretty output
        formatted = f"{Style.BRIGHT}{log_color}{record.levelname:<8}{Style.RESET_ALL} {record.getMessage()}"
        return f"{time_str} | {formatted}"


# ============================================================
# File Handler (Rotates Daily, keeps 7 days)
# ============================================================
file_handler = TimedRotatingFileHandler(
    filename="logs/app.log",
    when="midnight",      # rotate logs every midnight
    interval=1,           # every 1 day
    backupCount=7,        # keep 7 days of history
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)


# ============================================================
# Console Handler (Colorized Output)
# ============================================================
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())


# ============================================================
# Main Application Logger
# ============================================================
logger = logging.getLogger("support-chatbot")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ============================================================
# Specialized Sub-Loggers for Events
# ============================================================
# Lead capture events
lead_logger = logging.getLogger("lead-events")
lead_logger.setLevel(logging.INFO)
lead_logger.addHandler(file_handler)
lead_logger.addHandler(console_handler)

# Email escalation events
email_logger = logging.getLogger("email-events")
email_logger.setLevel(logging.INFO)
email_logger.addHandler(file_handler)
email_logger.addHandler(console_handler)

# Chat messages (conversations and user queries)
chat_logger = logging.getLogger("chat-events")
chat_logger.setLevel(logging.INFO)
chat_logger.addHandler(file_handler)
chat_logger.addHandler(console_handler)


# ============================================================
# Startup Confirmation Messages
# ============================================================
logger.info("🧠 Logging initialized. Writing to logs/app.log")
logger.info("💬 Chat, lead, and email loggers are active.")
