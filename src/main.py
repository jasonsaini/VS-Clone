from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import * 
from PyQt5.QtGui import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("VSClone")
        self.resize(1300, 900)
        
        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        
        self.window_font= QFont("Fire Code")
        self.window_font.setPointSize(16)
        self.setFont(self.window_font)
        
        self.setup_menu()
        self.setup_body()
        
        self.show()
        
    def setup_menu(self):
        pass
    
    def setup_body(self):
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
    sys.exit(0)