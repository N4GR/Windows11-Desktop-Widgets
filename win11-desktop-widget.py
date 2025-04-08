from src.application.application import Application
from src.windows.main_window import MainWindow

if __name__ == "__main__":
    application = Application()
    
    main_window = MainWindow()
    main_window.show()
    
    application.exec()