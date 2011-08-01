#external
from coordination.wire import Entity, Aspect
from coordination.runtime import Action

__all__ = ["StatusBar"]

class StatusBar(Entity):

    class QtWidget(Aspect):
        features = ("GUI.Qt",)
        def __init__(self, entity):
            super(StatusBar.QtWidget, self).__init__(entity)
            QtGui = self.entity.provider.QtGui
            self.__widget = QtGui.QStatusBar()
        @property
        def widget(self):
            return self.__widget

    class GtkWidget(Aspect):
        features = ("GUI.Gtk",)
        def __init__(self, entity):
            super(StatusBar.GtkWidget, self).__init__(entity)
            gtk = self.entity.provider.gtk
            widget = self.__widget = gtk.Statusbar()
            widget.show()
        @property
        def widget(self):
            return self.__widget

    class EditorKind(Aspect):
        features = ('Editor.Multiple')
        @Action.wrap
        def setKind(self, kind): pass

    class EditorPosition(Aspect):
        @Action.wrap
        def setPosition(self, col, row, number): pass

    class EditorFocus(Aspect):
        @Action.wrap
        def touch(self): pass

    class EditorSizes(Aspect):
        @Action.wrap
        def setSizes(self, chars, words, lines): pass
