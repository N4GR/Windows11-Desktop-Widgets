# Third-party imports.
from PySide6.QtWidgets import (
    QWidget, QApplication, QSystemTrayIcon, QMenu, QLabel,
    QHBoxLayout
)

from PySide6.QtCore import (
    Qt, QPoint, QUrl, QSize, QTimer
)

from PySide6.QtGui import (
    QIcon, QAction, QMouseEvent, QPixmap
)

from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

# Local imports.
from src.application.application import Application
from src.application.managers.network_manager import NetworkManager

from src.shared.funcs import *