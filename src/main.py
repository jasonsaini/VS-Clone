from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import * 
from PyQt5.QtGui import *

from pathlib import Path

import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_color = "#282c34"
        self.init_ui()
        
        self.current_file = None
    
    def init_ui(self):
        self.setWindowTitle("Visual Studio Clone")
        self.resize(1300, 900)
        
        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        
        self.window_font= QFont("Fire Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        self.setup_menu()
        self.setup_body()
        
        self.show()
    
    def get_editor(self) -> QsciScintilla:
        text_editor = QsciScintilla()
        
        text_editor.setUtf8(True)
        
        text_editor.setFont(self.window_font)
        
        text_editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
    
        text_editor.setIndentationGuides(True)
        text_editor.setTabWidth(4)
        text_editor.setIndentationsUseTabs(False)
        text_editor.setAutoIndent(True)
        
        # EOL
        text_editor.setEolMode(QsciScintilla.EolWindows)
        text_editor.setEolVisibility(False)
        
        # autocomplete
        # TODO: Add autocomplete
        
        #caret 
        # TODO: Add caret settings
        
        # lexer
        # TODO: Add lexer
        return text_editor
    
    def setup_status_bar(self):
        stat = QStatusBar(self)
        stat.setStyleSheet("color: #D3D3D3;")
        stat.showMessage("Ready", 3000)
        self.setStatusBar(stat)
    
    def setup_menu(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)
        
        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        
        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        
    def new_file(self):
        pass
        
    def open_file(self):
        pass
        
    def open_folder(self):
        pass
       
    def copy(self):
        pass
    
    def set_new_tab(self, path: Path, is_new_file=False):
        if not path.is_file():
            return
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary file", 2000)
            return

        # check if file already open
        if not is_new_file:
            for i in range(self.tab_view.count()):
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
        
        text_editor = self.get_editor()
        self.tab_view.addTab(text_editor, path.name)
        if not is_new_file:
            text_editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)
    def setup_body(self):
        # Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0,0,0,0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(0)
        body_frame.setLayout(body)
        
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(f'''
                                    background-color: {self.side_bar_color};
                                    ''')
        side_bar_layout = QHBoxLayout()
        side_bar_layout.setContentsMargins(5,10,5,0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        
        folder_label = QLabel()
        folder_label.setPixmap(QPixmap("./src/icons/folder-icon.svg").scaled(QSize(25,25)))
        folder_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        folder_label.mousePressEvent = self.show_hide_tab
        side_bar_layout.addWidget(folder_label)
        self.side_bar.setLayout(side_bar_layout)
        
        body.addWidget(self.side_bar)
        
        self.hsplit = QSplitter(Qt.Horizontal)

        # file manager frame & layout
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMaximumHeight(900)
        self.tree_frame.setBaseSize(100,0)
        self.tree_frame.setContentsMargins(0,0,0,0)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0,0,0,0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet('''
                                      QFrame{
                                          background-color: #21252b;
                                          border-radius: 5px;
                                          border: none;
                                          padding: 5px;
                                          color: #D3D3D3;
                                      }
                                      QFrame:hover{
                                          color:white;
                                      }
                                      ''')
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("FiraCode", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        
        # add context menu
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        #  click handling
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1,True)
        self.tree_view.setColumnHidden(2,True)
        self.tree_view.setColumnHidden(3,True)
        
        #setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)
        
        #add tab window
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0,0,0,0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        
        
        
        self.hsplit.addWidget(self.tree_frame)
        self.hsplit.addWidget(self.tab_view)
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)
        
        self.setCentralWidget(body_frame)
    
    def show_hide_tab(self):
        ...
    
    def tree_view_context_menu(self,pos):
        ...
    def tree_view_clicked(self, index:QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)
    
    def is_binary(self, path):
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
    sys.exit(0)