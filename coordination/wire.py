#standart
from weakref import proxy
from collections import defaultdict
#internal
from .runtime import Actor 

class Aspect(Actor):
    features = ()
    def __init__(self, entity):
        super(Aspect, self).__init__()
        self.entity = proxy(entity)
        entity.register_aspect(self)
    @classmethod
    def check(self, entity):
        for feature in self.features:
            if not entity.exists(feature):
                return False
        return True

class Entity(object):
    provider = None
    scope = None
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
        if cls.provider is None:
            return False
        else:
            return feature in cls.provider

    def register_entity(self):
        if self.scope is not None:
            self.scope.register_entity(self)

    def register_aspect(self, aspect):
        if self.scope is not None:
            self.scope.register_aspect(self, aspect)

class Coordinator(Actor):
    def __del__(self):
        self.destroy()
        
    def create(self): pass
    def destroy(self): pass