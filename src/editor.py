from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

class Editor(QsciScintilla):

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

          
        self.setUtf8(True)
        
        self.window_font = QFont("Fire Code") # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        self.setFont(self.window_font)
        
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
    
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        
        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)
        
        #caret 
        # TODO: Add caret settings
        #!self.setCaretForegroundColor(QColor("#dedcdc"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
       # self.setCaretLineBackgroundColor(QColor("#2c313c"))
        
        #autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        # minimum character before autocomplete shows
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # lexer/syntax highlighting
        # TODO: Expand functionality of default python lexer
        self.python_lexer = QsciLexerPython()
        
        '''
        self.api = QsciAPIs(self.python_lexer)
        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)
        
        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)
            
        self.api.add("addition(a: int, b: int)")
        
        self.api.prepare()
        '''
        
        # line numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

        self.setLexer(self.python_lexer)
        
        #self.keyPressEvent = self.handle_editor_press
        
        #return self
    
    def handle_editor_press(self, e: QKeyEvent):
        self:QsciScintilla = self.tab_view.currentWidget()
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            QsciScintilla.keyPressEvent(self, e)
    
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
        
