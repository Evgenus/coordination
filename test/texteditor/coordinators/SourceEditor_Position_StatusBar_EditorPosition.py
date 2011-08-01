#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_SourceEditor_Position_StatusBar_EditorPosition"
    ]

class Coordinator_SourceEditor_Position_StatusBar_EditorPosition(Coordinator):
    require = [
        ('SourceEditor', 'Position'),
        ('StatusBar', 'EditorPosition'),
        ]
    def __init__(self, aspect_position, aspect_statusbar):
        self.aspect_position = aspect_position
        self.aspect_statusbar = aspect_statusbar

    def create(self):
        self.aspect_position.changed << self.aspect_statusbar.setPosition

