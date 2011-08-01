#standart
import sys
import time
#external
from coordination.wire import Entity, Aspect
from coordination.runtime import MessageLoop

__all__ = ["Reactor"]

class Reactor(Entity):

    class Gtk(Aspect, MessageLoop):
        features = ("GUI.Gtk",)
        def run(self):
            gtk = self.entity.provider.gtk
            while True:
                while gtk.events_pending():
                    gtk.main_iteration(False)
                if not self.callback():
                    time.sleep(self.timeout)

    class Qt(Aspect, MessageLoop):
        features = ("GUI.Qt",)
        def __init__(self, *args, **kwargs):
            super(Reactor.Qt, self).__init__(*args, **kwargs)
            QtGui = self.entity.provider.QtGui
            self.app = QtGui.QApplication(sys.argv)

        def run(self): 
            while True:
                self.app.processEvents()
                if not self.callback():
                    time.sleep(self.timeout)
