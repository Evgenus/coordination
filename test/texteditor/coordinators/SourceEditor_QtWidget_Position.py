#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_SourceEditor_QtWidget_Position"
    ]

class Coordinator_SourceEditor_QtWidget_Position(Coordinator):
    require = [
        ('SourceEditor', 'QtWidget', 'Position'),
        ]
    def __init__(self, aspect_widget, aspect_position):
        self.aspect_widget = aspect_widget
        self.aspect_position = aspect_position

    def create(self):
        widget = self.aspect_widget.widget
        widget.cursorPositionChanged.connect(self.cursorPositionChanged)

    def cursorPositionChanged(self):
        widget = self.aspect_widget.widget
        cursor = widget.textCursor()
        col = cursor.positionInBlock()+1
        row = cursor.blockNumber()+1
        pos = cursor.position()
        document = widget.document()
        if 0<=pos<document.characterCount():
            char = document.characterAt(pos)
            number = char.unicode()
        else:
            number = None
        self.aspect_position.changed(col, row, number)
