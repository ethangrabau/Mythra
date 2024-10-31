# memory_manager.py
class MemoryManager:
    def __init__(self):
        self.recent_memory = []
        self.long_term_memory = []

    def set_recent_memory(self, memory):
        """Set the recent memory."""
        self.recent_memory = [memory]

    def set_long_term_memory(self, memory):
        """Set the long-term memory."""
        self.long_term_memory = [memory]

    def get_recent_memory(self):
        """Return a concatenated version of recent memory."""
        return "\n".join(self.recent_memory)

    def get_long_term_memory(self):
        """Return a concatenated version of long-term memory."""
        return "\n".join(self.long_term_memory)
