#standart
from functools import partial
from weakref import proxy
from collections import deque, defaultdict

class FeatureChecker(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, subj):
        try:
            self.func(subj)
        except Exception as error:
            subj.forbid(self.name)
        else:
            subj.allow(self.name)

class FeaturesProvider(object):
    'Holding information about available system features for aspects'
    checkers = {}
    def __init__(self):
        self.features = {}
        self.namespace = {}
        for name, checker in self.checkers.iteritems():
            checker(self)
    def __contains__(self, feature):
        return self.features.get(feature, False)
    def allow(self, name):
        self.features[name] = True
    def forbid(self, name):
        self.features[name] = False
    def provide(self, **kwargs):
        self.namespace.update(kwargs)
    def __getattr__(self, name):
        if name in self.namespace:
            return self.namespace[name]
        raise AttributeError(name)
    @classmethod
    def feature(cls, name):
        return partial(FeatureChecker, name)

class FeaturesProviderMeta(type):
    def __new__(meta, name, bases, internals):
        checkers = {}
        cls = type.__new__(meta, name, bases, internals)
        checkers.update(cls.checkers)
        for name, value in internals.iteritems():
            if isinstance(value, FeatureChecker):
                checkers[name] = value
        cls.checkers = checkers
        return cls

FeaturesProvider = FeaturesProviderMeta('FeaturesProvider', 
    FeaturesProvider.__bases__, dict(FeaturesProvider.__dict__))

class MessageQueue(object):
    'Events queue for actors'
    def __init__(self):
        self.queue = deque()
    def add(self, callable, *args, **kwargs):
        item = partial(callable, *args, **kwargs)
        self.queue.append(item)
    def __call__(self):
        if self.queue:
            callable = self.queue.popleft()
            callable()
            return True
        else:
            return False

class MessageLoop(object):
    'Base abstract class for event-loop'
    timeout = 0.01
    def set_callback(self, callback):
        self.callback = callback
    def run(self): 
        raise NotImplementedError()
    def callback(self):
        return False


class Action(object):
    'Basic concurency primitive'
    queue = None
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
            if self.queue is not None:
                self.queue.add(callback, *args, **kwargs)
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
        super(Actor, self).__init__()
        for name, cls_action in self._actions.iteritems():
            action = cls_action.clone()
            cls_action << action
            action.source = proxy(self)
            setattr(self, name, action)

class MotherOfObjects(object):
    def __init__(self):
        self.entities = defaultdict(list)
        self.aspects = defaultdict(list)

    def register_entity(self, entity):
        self.entities[type(entity)].append(entity)
        
    def register_aspect(self, entity, aspect):
        self.aspects[type(entity), type(aspect)].append(aspect)
