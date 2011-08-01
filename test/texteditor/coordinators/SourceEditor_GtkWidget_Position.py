#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_SourceEditor_GtkWidget_Position"
    ]

class Coordinator_SourceEditor_GtkWidget_Position(Coordinator):
    require = [
        ('SourceEditor', 'GtkWidget', 'Position'),
        ]
    def __init__(self, aspect_widget, aspect_position):
        self.aspect_widget = aspect_widget
        self.aspect_position = aspect_position

    def create(self):
        widget = self.aspect_widget.widget
        buffer = widget.get_buffer()
        widget.connect_after('move-cursor', self.cursorPositionChanged)
        buffer.connect_after('changed', self.cursorPositionChanged)

    def cursorPositionChanged(self, *args):
        widget = self.aspect_widget.widget
        buffer = widget.get_buffer()
        offset = buffer.get_property('cursor-position')
        iter = buffer.get_iter_at_offset(offset)
        col = iter.get_line_index() + 1
        row = iter.get_line() + 1
        char = iter.get_char()
        self.aspect_position.changed(col, row, ord(char))

