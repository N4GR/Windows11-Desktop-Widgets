# Python imports.
import json

# Third-party imports.
from PySide6.QtWidgets import (
    QApplication
)

from PySide6.QtCore import (
    QUrl
)

from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

class NetworkManager(QNetworkAccessManager):
    def __init__(
            self,
            parent: QApplication
    ):
        super().__init__(parent)
    
    def send_get_request(
            self,
            url: str
    ) -> None:
        """Create a get request to a given url."""
        print(f"NetworkManager | GET | {url}")
        
        # Set the URL as a QURL.
        url = QUrl(url)
        
        # Create a request object from the QURL.
        request = QNetworkRequest(url)
        
        # Send a get request.
        self.get(request)
    
    def get_reply_data(
            self,
            reply: QNetworkReply
    ) -> dict | None:
        """Get the data from a network manager reply.

        Args:
            reply (QNetworkReply): Reply from the network manager.

        Returns:
            dict | None: Dictionary of data in the reply, none if error.
        """
        if reply.error() == QNetworkReply.NetworkError.NoError:
            # If there's no error in the reply.
            response_data = reply.readAll()
            data = json.loads(response_data.data().decode())
            
            # Delete the reply object.
            reply.deleteLater()
            
            # Return the dictionary data.
            return data
        
        else:
            print(f"Network reply error: {reply.error().name} {reply.error().value}")
            
            # Delete the reply object.
            reply.deleteLater()
            
            # Return non on error.
            return None