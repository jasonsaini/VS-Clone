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
        
        #caret 
        # TODO: Add caret settings
        text_editor.setCaretForegroundColor(QColor("#dedcdc"))
        text_editor.setCaretLineVisible(True)
        text_editor.setCaretWidth(2)
        text_editor.setCaretLineBackgroundColor(QColor("#2c313c"))
        
        #autocomplete
        text_editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        # minimum character before autocomplete shows
        text_editor.setAutoCompletionThreshold(1)
        text_editor.setAutoCompletionCaseSensitivity(False)
        #text_editor.setAutoCompletionUseSingle(QsciScintilla.AcuNever)

                
        # lexer/syntax highlighting
        # TODO: Expand functionality of default python lexer
        python_lexer = QsciLexerPython()
        text_editor.setLexer(python_lexer)
        
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
        
        file_menu.addSeparator()
        
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        
        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_file_as)
        

        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        
    def new_file(self):
        self.set_new_tab(Path("untitled"), is_new_file=True)
        
    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0 :
            self.save_file_as()
        
        text_editor = self.tab_view.currentWidget()
    
    def save_file_as(self):
        text_editor = self.tab_view.currentWidget()
        if text_editor is None:
            return
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == "":
            self.statusBar().showMessage("Save cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(text_editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path
        
    def open_file(self):
        options  = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        new_file, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Python Files (*.py)", options=options)
        
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        opened_filepath = Path(new_file)
        self.set_new_tab(opened_filepath)
        
        
    def open_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        
        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=options)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)
       
    def copy(self):
        text_editor = self.tab_view.currentWidget()
        if text_editor is not None:
            text_editor.copy()
            
    def set_new_tab(self, path: Path, is_new_file=False):
        text_editor = self.get_editor()
        
        if is_new_file:
            self.tab_view.addTab(text_editor, "untitled")
            self.setWindowTitle("untitled")
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return
        
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
        
        # add tab closing
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        
        
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
    
    def close_tab(self,index):
        self.tab_view.removeTab(index)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
    sys.exit(0)