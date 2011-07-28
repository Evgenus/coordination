import sys
import time
from collections import deque, defaultdict
from functools import partial
from weakref import proxy

class FeaturesProvider(object):
    features = {}
    def check(self, feature):
        return self.features.get(feature, False)
    @classmethod
    def allow(self, name):
        self.features[name] = True
    @classmethod
    def forbid(self, name):
        self.features[name] = False

try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    FeaturesProvider.forbid("GUI.Qt")
else:
    pass
    FeaturesProvider.allow("GUI.Qt")

class Scheduler(object):
    def __init__(self):
        self.queue = deque()
    def add(self, callable, *args, **kwargs):
        item = partial(callable, *args, **kwargs)
        self.queue.append(item)
    def tick(self):
        if self.queue:
            callable = self.queue.popleft()
            callable()
            return True
        else:
            return False

class Action(object):
    scheduler = None
    def __init__(self, preprocess=None):
        self.preprocess = preprocess
        self.callbacks = []
        self.source = None
        self.name = None

    def __lshift__(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)
        return self
    def __rshift__(self, callback):
        if callback in self.callbacks:
            self.callbacks.append(callback)
        return self
    def clear(self):
        self.callbacks = []
    def __repr__(self):
        return "<Action {0} of {1}>".format(self.name, self.source)
    def __call__(self, *args, **kwargs):
        if self.preprocess is not None:
            result = self.preprocess(self.source, *args, **kwargs)
            if result is not None:
                args, kwargs = result
        for callback in self.callbacks:
            if self.scheduler is not None:
                self.scheduler.add(callback, *args, **kwargs)
            else:
                callback(*args, **kwargs)
    def clone(self):
        new = self.__class__(self.preprocess)
        new.name = self.name
        return new

    @classmethod
    def wrap(cls, callable):
        return cls(callable)

class Actor(object):
    class __metaclass__(type):
        def __new__(meta, name, bases, internals):
            actions = internals['_actions'] = {}
            for key, value in internals.iteritems():
                if isinstance(value, Action):
                    actions[key] = value
            cls = type.__new__(meta, name, bases, internals)
            for key, action in actions.iteritems():
                action.source = proxy(cls)
                action.name = key
            return cls
    def __init__(self):
        for name, cls_action in self._actions.iteritems():
            action = cls_action.clone()
            cls_action << action
            action.source = proxy(self)
            setattr(self, name, action)

class Aspect(Actor):
    features = ()
    def __init__(self, entity):
        self.entity = proxy(entity)
        entity.register_aspect(self)
    @classmethod
    def check(self, entity):
        for feature in self.features:
            if not entity.exists(feature):
                return False
        return True

class Entity(object):
    features_provider = None
    mother = None
    class __metaclass__(type):
        def __new__(meta, name, bases, internals):
            aspects = internals['_aspects'] = {}
            for key, value in internals.iteritems():
                if isinstance(value, type) and issubclass(value, Aspect):
                    aspects[key] = value
            cls = type.__new__(meta, name, bases, internals)                
            return cls
    def __init__(self):
        self.provided = defaultdict(list)
        for name, aspect_type in self._aspects.iteritems():
            if aspect_type.check(self):
                setattr(self, name, aspect_type(self))
                self.provided[aspect_type].append(name)
        self.register_entity()

    @classmethod
    def exists(cls, feature):
        if cls.features_provider is None:
            return False
        else:
            return cls.features_provider.check(feature)

    def register_entity(self):
        if self.mother is not None:
            self.mother.register_entity(self)

    def register_aspect(self, aspect):
        if self.mother is not None:
            self.mother.register_aspect(self, aspect)

class Coordinator(Actor):
    def __del__(self):
        self.destroy()
        
    def create(self): pass
    def destroy(self): pass

class MotherOfObjects(object):
    def __init__(self):
        self.entities = defaultdict(list)
        self.aspects = defaultdict(list)

    def register_entity(self, entity):
        self.entities[type(entity)].append(entity)
        
    def register_aspect(self, entity, aspect):
        self.aspects[type(entity), type(aspect)].append(aspect)

# ____________________________________________________________________________ #

class StatusBar(Entity):

    class QtWidget(Aspect):
        features = ("GUI.Qt",)
        def __init__(self, entity):
            super(StatusBar.QtWidget, self).__init__(entity)
            self.__widget = QtGui.QStatusBar()
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

class Coordinator_StatusBar_EditorPosition_QtWidget:
    def __init__(self, aspect_editorposition, aspect_widget):
        self.aspect_editorposition = aspect_editorposition
        self.aspect_widget = aspect_widget
    
    def create(self):
        widget = self.aspect_widget.widget
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

class SourceEditor(Entity):

    class QtWidget(Aspect):
        features = ("GUI.Qt",)
        def __init__(self, entity):
            super(SourceEditor.QtWidget, self).__init__(entity)
            self.__widget = QtGui.QTextEdit()
        @property
        def widget(self):
            return self.__widget

    class Position(Aspect):
        @Action.wrap
        def changed(self, col, row, number): pass

    class Focus(Aspect):
        @Action.wrap
        def focusChanged(self, focused): pass

class Coordinator_SourceEditor_QtWidget_Position(Coordinator):
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

class Coordinator_SourceEditor_Position_StatusBar_EditorPosition(Coordinator):
    def __init__(self, aspect_position, aspect_statusbar):
        self.aspect_position = aspect_position
        self.aspect_statusbar = aspect_statusbar

    def create(self):
        self.aspect_position.changed << self.aspect_statusbar.setPosition

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    # Dependency Injection
    scheduler = Action.scheduler = Scheduler()
    mother = Entity.mother = MotherOfObjects()
    Entity.features_provider = FeaturesProvider()

    statusbar = StatusBar()
    
    editor = SourceEditor()
    
    coorditators = [
        Coordinator_StatusBar_EditorPosition_QtWidget(
            statusbar.EditorPosition, statusbar.QtWidget),
        Coordinator_SourceEditor_Position_StatusBar_EditorPosition(
            editor.Position, statusbar.EditorPosition),
        Coordinator_SourceEditor_QtWidget_Position(
            editor.QtWidget, editor.Position)
        ]
        
    for coordinator in coorditators:
        coordinator.create()
    
    mainWin = QtGui.QMainWindow()
    mainWin.setStatusBar(statusbar.QtWidget.widget)
    mainWin.setCentralWidget(editor.QtWidget.widget)
    mainWin.show()
    
    while True:
        app.processEvents()
        scheduler.tick()
        time.sleep(0.01)
