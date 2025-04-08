from src.shared.imports import *

class BitCoinWidget(QWidget):
    def __init__(
            self,
            parent: QWidget
    ) -> None:
        super().__init__(parent)
        
        self.api_url = "https://api.coingecko.com/api/v3/simple/"
        
        self.crypto_endpoint = "price?ids="
        self.cryptos = ["bitcoin"]
        
        self.currency_endpoint = "vs_currencies="
        self.currencies = ["gbp"]
        
        self.request_interval = 300 # 5 minutes, 300 seconds.
        self.remaining_time = self.request_interval # Keep track of time remaining.
        
        self._set_design()
        self._set_widgets()
        self._set_layout()
        
        # Get the network manager from the application.
        self.network_manager : NetworkManager = QApplication.instance().property("NetworkManager")
        self.network_manager.finished.connect(self._get_network_reply)
        
        # Create a timer to activate every x milliseconds.
        self.timer = QTimer(self)
        self.timer.setInterval(1000) # Every second.
        self.timer.timeout.connect(self._on_timer_timeout) # Update timer label.
        self.timer.start() # Start the timer loop.
        
        self.request() # Create a request on startup.
    
    def _set_design(self):
        self.setFixedWidth(self.parentWidget().width())
        self.setFixedHeight(50)
        
    def _set_widgets(self):
        self.background_label = BackgroundLabel(self)
        self.crypto_icon = CryptoIcon(self, "bitcoin")
        self.price_label = PriceLabel(self, 100)
        self.timer_label = TimerLabel(self, self.request_interval)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        
        self.main_layout.addWidget(self.crypto_icon)
        self.main_layout.addWidget(self.price_label)
        self.main_layout.addWidget(self.timer_label, alignment = Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.main_layout)
    
    def _on_timer_timeout(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        
        time_str = f"{minutes:02}:{seconds:02}"
        self.timer_label.setText(time_str) # Set timer string to text label.
        
        # Decreate the remaining time by one second.
        self.remaining_time -= 1
        
        # If the remaining time goes to 0.
        if self.remaining_time <= 0:
            self.request() # Make a request.
            
            # Reset the remaining time.
            self.remaining_time = self.request_interval
    
    def request(self):
        url = (
            f"{self.api_url}"
            f"{self.crypto_endpoint}"
            f"{','.join(self.cryptos)}"
            f"&{self.currency_endpoint}"
            f"{','.join(self.currencies)}"
        )
        
        self.network_manager.send_get_request(url)
    
    def _get_network_reply(
            self,
            reply: QNetworkReply
    ) -> None:
        # Get the reply data using the network manager.
        reply_data = self.network_manager.get_reply_data(reply)
        
        bitcoin_price = float(reply_data["bitcoin"]["gbp"]) # Get number as float.
        formatted_price = f"{bitcoin_price:,.2f}" # 9999.9 -> 9,999.90
        
        self.price_label.setText(f"£{formatted_price}")

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

class CryptoIcon(QLabel):
    def __init__(
            self,
            parent: QWidget,
            crypto_name: str
    ) -> None:
        super().__init__(parent)
        self.crypto_name = crypto_name
        
        self._set_design()
    
    def _set_design(self):
        size = min(self.parentWidget().height(), self.parentWidget().width())
        new_size = QSize(size, size)
        
        self.setFixedSize(new_size)
        self.setPixmap(
            QPixmap(
                path("/assets/icons/bitcoin.png")
            ).scaled(
                QSize(
                    size - 10,
                    size - 10
                ),
                aspectMode = Qt.AspectRatioMode.KeepAspectRatio,
                mode = Qt.TransformationMode.SmoothTransformation
            )
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class PriceLabel(QLabel):
    def __init__(
            self,
            parent: QWidget,
            price: int
    ) -> None:
        super().__init__(
            parent,
            text = str(price)
        )
        
        self.price = price
        
        self.setStyleSheet(
            "color: white;"
        )

class TimerLabel(QLabel):
    def __init__(
            self,
            parent: QWidget,
            time: int
    ) -> None:
        super().__init__(parent)
        minutes = time // 60
        seconds = time % 60
        
        time_str = f"{minutes:02}:{seconds:02}"
        
        self.setText(time_str)
        
        self.setStyleSheet(
            "color: white;"
        )
        