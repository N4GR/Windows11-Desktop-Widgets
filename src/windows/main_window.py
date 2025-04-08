from src.shared.imports import *

# Widget imports.
from src.windows.widgets.bitcoin_widget import BitCoinWidget

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._set_design()
        self._set_widgets()
        
        self.drag_position = None # Keep track of drag position.
    
    def _set_design(self):
        self.setFixedSize(200, 50)
        
        # Move the widget to the old position from data.
        self.move(self.load_old_position())
        
        # In case the window needs a title.
        self.setWindowTitle("BitCoin Desktop Widget")
        
        # In case the window needs an icon.
        self.setWindowIcon(QPixmap(path("/assets/icons/bitcoin.png")))
        
        # Setting windows flags and attributes.
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.WindowStaysOnBottomHint |
            Qt.WindowType.FramelessWindowHint
        )
        
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
    
    def _set_widgets(self):
        self.background_label = BackgroundLabel(self)
        self.system_tray = SystemTray(self)
        
        self.bitcoin_widget = BitCoinWidget(self)
    
    def load_old_position(self) -> QPoint:
        json_data = load_json_data(path("/data/position.json"))
        
        return QPoint(
            json_data["x"],
            json_data["y"]
        )
    
    def update_position_data(
            self,
            point: QPoint
    ):
        update_json_data(
            path("/data/position.json"),
            data = {
                "x": point.x(),
                "y": point.y()
            }
        )
    
    def mousePressEvent(
            self,
            event: QMouseEvent
    ):
        if event.button() == Qt.MouseButton.LeftButton:
            # Store the point where the mouse was pressed.
            self.drag_position = event.globalPosition().toPoint()
            
            # Update the poision in the data json.
            self.update_position_data(self.pos())
        
        return super().mousePressEvent(event)

    def mouseMoveEvent(
            self,
            event: QMouseEvent
    ):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            # Calculate distance moved and move the window.
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            
            # Update the poision in the data json.
            self.update_position_data(self.pos())
        
        return super().mouseMoveEvent(event)

class BackgroundLabel(QLabel):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        self._set_design()
    
    def _set_design(self):
        self.setFixedSize(self.parentWidget().size())
        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.5);"
            "border-radius: 15px;"
        )

class SystemTray(QSystemTrayIcon):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        self._set_icon()
        self._set_actions()
        self._set_menu()
    
    
    def _set_icon(self):
        self.setIcon(QIcon(path("/assets/icons/bitcoin.png")))
        self.setVisible(True)
    
    def _set_actions(self):
        self.close_action = QAction("Quit", self)
        self.close_action.triggered.connect(self._close_action_clicked)
    
    def _set_menu(self):
        self.menu = QMenu(self.parent())
        
        # Add actions.
        self.menu.addAction(self.close_action)
        
        # Set menu to tray icon.
        self.setContextMenu(self.menu)
    
    def _close_action_clicked(self):
        # Close the application.
        QApplication.quit()