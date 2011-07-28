import sys
import time

class Reactor(object):
    timeout = 0.01
    def __init__(self, callback):
        self.callback = callback
    def run(self): 
        raise NotImplementedError()

# ____ GTK+

import pygtk
pygtk.require('2.0')
import gtk
import gobject

class GtkReactor(Reactor):
    def run(self):
        while True:
            while gtk.events_pending():
                gtk.main_iteration(False)
            if not self.callback():
                time.sleep(self.timeout)

# ____ Qt

from PyQt4 import QtGui

class QtReactor(Reactor):
    def __init__(self, *args, **kwargs):
        super(QtReactor, self).__init__(*args, **kwargs)
        self.app = QtGui.QApplication(sys.argv)

    def run(self): 
        while True:
            self.app.processEvents()
            if not self.callback():
                time.sleep(self.timeout)

def func():
    print 1

if __name__ == "__main__":
    GtkReactor(func).run()
