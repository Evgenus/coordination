#external
from coordination.runtime import FeaturesProvider as Provider
from coordination.runtime import MotherOfObjects
from coordination.wire import Entity
# internal
import coordinators
import entities

class FeaturesProvider(Provider):

    @Provider.feature('GUI.Qt')
    def Qt(self):
        from PyQt4 import QtCore, QtGui
        self.provide(QtCore=QtCore, QtGui=QtGui)

    @Provider.feature('GUI.Gtk')
    def Gtk(self):
        import pygtk
        pygtk.require('2.0')
        import gtk
        import gobject
        self.provide(gtk=gtk)

def main():
    mother = Entity.mother = MotherOfObjects()
    provider = Entity.provider = FeaturesProvider()

    scheduler = entities.Scheduler()
    
    reactor = entities.Reactor()
    
    statusbar = entities.StatusBar()
        
    editor = entities.SourceEditor()

    if False:
        coorditators = [
            coordinators.Coordinator_StatusBar_EditorPosition_QtWidget(
                statusbar.EditorPosition, statusbar.QtWidget),
            coordinators.Coordinator_SourceEditor_Position_StatusBar_EditorPosition(
                editor.Position, statusbar.EditorPosition),
            coordinators.Coordinator_SourceEditor_QtWidget_Position(
                editor.QtWidget, editor.Position),
            coordinators.Coordinator_Reactor_Qt_Scheduler_Queue(
                reactor.Qt, scheduler.Queue),
            coordinators.Coordinator_Scheduler_Queue(
                scheduler.Queue),
            ]

        mainWin = provider.QtGui.QMainWindow()
        mainWin.setStatusBar(statusbar.QtWidget.widget)
        mainWin.setCentralWidget(editor.QtWidget.widget)
        mainWin.show()

        for coordinator in coorditators:
            coordinator.create()

        reactor.Qt.run()    

    else:
        coorditators = [
            coordinators.Coordinator_StatusBar_EditorPosition_GtkWidget(
                statusbar.EditorPosition, statusbar.GtkWidget),
            coordinators.Coordinator_SourceEditor_Position_StatusBar_EditorPosition(
                editor.Position, statusbar.EditorPosition),
            coordinators.Coordinator_SourceEditor_GtkWidget_Position(
                editor.GtkWidget, editor.Position),
            coordinators.Coordinator_Reactor_Gtk_Scheduler_Queue(
                reactor.Gtk, scheduler.Queue),
            coordinators.Coordinator_Scheduler_Queue(
                scheduler.Queue),
            ]

        mainWin = provider.gtk.Window()
        layout = provider.gtk.VBox(False, 0)
        layout.pack_start(editor.GtkWidget.widget, True, True, 0)
        layout.pack_start(statusbar.GtkWidget.widget, False, True, 0)
        layout.show()
        mainWin.add(layout)
        mainWin.show()

        for coordinator in coorditators:
            coordinator.create()

        reactor.Gtk.run()
