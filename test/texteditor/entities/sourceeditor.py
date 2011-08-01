#standart
from weakref import proxy
#external
from coordination.wire import Entity, Aspect
from coordination.runtime import Action

__all__ = ["SourceEditor"]

class SourceEditor(Entity):

    class QtWidget(Aspect):
        features = ("GUI.Qt",)
        def __init__(self, entity):
            super(SourceEditor.QtWidget, self).__init__(entity)
            QtGui = self.entity.provider.QtGui
            self.__widget = QtGui.QTextEdit()
        @property
        def widget(self):
            return self.__widget

    class GtkWidget(Aspect):
        features = ("GUI.Gtk",)
        def __init__(self, entity):
            super(SourceEditor.GtkWidget, self).__init__(entity)
            gtk = self.entity.provider.gtk
            widget = self.__widget = gtk.TextView()
            widget.set_editable(True)
            widget.show()
        @property
        def widget(self):
            return self.__widget

    class Position(Aspect):
        @Action.wrap
        def changed(self, col, row, number): pass

    class Focus(Aspect):
        @Action.wrap
        def focusChanged(self, focused): pass