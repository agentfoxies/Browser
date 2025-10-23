import os
import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

class AntiblockBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Antiblock Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create the main web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.setup_https()

        # URL bar and navigation buttons
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.browser.back)

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.browser.forward)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.browser.reload)

        nav_bar = QWidget()
        nav_layout = QVBoxLayout()
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_bar.setLayout(nav_layout)

        layout = QVBoxLayout()
        layout.addWidget(nav_bar)
        layout.addWidget(self.browser)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.browser.urlChanged.connect(self.update_url_bar)

    def setup_https(self):
        profile = self.browser.page().profile()
        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

    def load_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.browser.setUrl(url)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

def is_admin():
    """ Check if the script is run with admin privileges """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        # Re-run the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    app = QApplication(sys.argv)
    browser = AntiblockBrowser()
    browser.show()
    sys.exit(app.exec_())
