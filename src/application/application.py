from PySide6.QtWidgets import QApplication

# Manager imports.
from src.application.managers.network_manager import NetworkManager

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self._set_managers()
        self._set_properties()
    
    def _set_managers(self):
        """Load managers to self."""
        self.network_manager = NetworkManager(self)
    
    def _set_properties(self):
        """Set properties to the application."""
        self.setProperty("NetworkManager", self.network_manager)