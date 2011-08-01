#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_StatusBar_EditorPosition_GtkWidget"
    ]

class Coordinator_StatusBar_EditorPosition_GtkWidget(Coordinator):
    require = [
        ('StatusBar', 'EditorPosition', 'GtkWidget'),
        ]
    def __init__(self, aspect_editorposition, aspect_widget):
        self.aspect_editorposition = aspect_editorposition
        self.aspect_widget = aspect_widget
    
    def create(self):
        widget = self.aspect_widget.widget
        self.context_id = widget.get_context_id("Statusbar")
        self.aspect_editorposition.setPosition << self.setPosition

    def setPosition(self, col, row, num):
        widget = self.aspect_widget.widget
        if num is None or num==0:
            char = ''
            num = ''
            hex = ''
        else:
            char = chr(num)
            hex = '%04X' % num
        buf = "{0} | {1} | {2} | {3} | {4}".format(col, row, char, num, hex)
        widget.push(self.context_id, buf)
