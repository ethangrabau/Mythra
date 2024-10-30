import logging
from collections import defaultdict

class MemoryManager:
    def __init__(self):
        # Initialize memory as a dictionary with categories for characters, items, locations, and recent activity
        self.memory_table = {
            "characters": defaultdict(str),
            "items": defaultdict(str),
            "locations": defaultdict(str),
            "recent_activity_summary": "",
        }
        # Set up logger to ensure all log entries are written to the dnd_app_log.txt
        logging.basicConfig(
            filename="dnd_app_log.txt",
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )

    def update_memory(self, category, name, description):
        """Update a specific memory category with a new or existing entry."""
        if category in self.memory_table:
            self.memory_table[category][name] = description
            logging.info(f"Updated {category} memory for {name}: {description}")
            self.log_memory_table()  # Log memory table after each update

    def update_recent_activity(self, activity):
        """Update recent activity with new actions or descriptions."""
        self.memory_table["recent_activity_summary"] = activity
        logging.info(f"Updated recent activity: {activity}")
        self.log_memory_table()  # Log memory table after each update

    def log_memory_table(self):
        """Log the full current state of the memory table to the log file."""
        logging.info("Current Memory Table State:")
        for category, entries in self.memory_table.items():
            if isinstance(entries, dict):
                for name, description in entries.items():
                    logging.info(f"{category.capitalize()}: {name} - {description}")
            else:
                logging.info(f"{category.capitalize()}: {entries}")

    def get_memory(self):
        """Return the entire memory table."""
        return self.memory_table
    
    def clear_memory(self):
        # Clear all memory entries
        self.memory = {
            'characters': defaultdict(str),
            'items': defaultdict(str),
            'locations': defaultdict(str),
            'recent_activity_summary': ''
        }
