#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_StatusBar_EditorPosition_QtWidget"
    ]

class Coordinator_StatusBar_EditorPosition_QtWidget(Coordinator):
    require = [
        ('StatusBar', 'EditorPosition', 'QtWidget'),
        ]
    def __init__(self, aspect_editorposition, aspect_widget):
        self.aspect_editorposition = aspect_editorposition
        self.aspect_widget = aspect_widget
    
    def create(self):
        widget = self.aspect_widget.widget
        QtGui = self.aspect_widget.entity.provider.QtGui
        self.col = QtGui.QLabel()
        self.row = QtGui.QLabel()
        self.char_view = QtGui.QLabel()
        self.char_number = QtGui.QLabel()
        self.char_hex_code = QtGui.QLabel()
        widget.addWidget(self.col)
        widget.addWidget(self.row)
        widget.addWidget(self.char_view)
        widget.addWidget(self.char_number)
        widget.addWidget(self.char_hex_code)
        self.aspect_editorposition.setPosition << self.setPosition

    def setPosition(self, col, row, number):
        QtCore = self.aspect_widget.entity.provider.QtCore
        self.col.setNum(col)
        self.row.setNum(row)
        if number is not None:
            char = QtCore.QChar(number)
            self.char_view.setText(char)
            self.char_number.setNum(number)
            self.char_hex_code.setText('%04X' % number)
        else:
            self.char_view.clear()
            self.char_number.clear()
            self.char_hex_code.clear()

    def destroy(self):
        widget = self.aspect_widget.widget
        widget.removeWidget(self.col)
        widget.removeWidget(self.row)
        widget.removeWidget(self.char_view)
        widget.removeWidget(self.char_number)
        widget.removeWidget(self.char_hex_code)