from collections import defaultdict
import re

class Rule(object):
    def __init__(self):
        self.left = set(self.keys)
        self.found = {}

    def add(self, key, obj):
        self.left.remove(key)
        index = self.keys.index(key)
        self.found[index] = obj
        if self.left:
            return False
        args = []
        for index in range(len(self.found)):
            args.append(self.found[index])
        self.callback(*args)
        return True

    def callback(self, *args, **kwargs):
        pass

    def __contains__(self, key):
        return key in self.left

    def __repr__(self):
        return "<{0} {1} of {2}>".format(
            self.__class__.__name__,
            self.left, self.keys)

class Scope(object):
    def __init__(self, name):
        self.name = name
        self.types = defaultdict(list)
        self.stack = defaultdict(list)
        self.storage = defaultdict(list)

    def add_rule(self, cb, *args):
        class rule(Rule):
            keys = map(Key.create, args)
            callback = cb
        print '{0}.add_rule({1})'.format(self.name, rule.keys)
        isolator = self.__class__(self.name + '-isolator')
        for key in rule.keys:
            self.types[key].append(rule)
            isolator.types[key].append(rule)
        for key in rule.keys:
            for item in self.storage[key]:
                isolator.add_key(*item)
        for instance in isolator.stack[rule]:
            self.stack[rule].append(instance)

    def create(self, rule, key, obj):
        instance = rule()
        self.stack[rule].append(instance)
        instance.add(key, obj)
        return instance

    def accept(self, instance, key, obj):
        if instance.add(key, obj):
            self.stack[type(instance)].remove(instance)

    def add_key(self, key, obj):
        print '{0}.add_key({1})'.format(self.name, key)
        self.storage[key].append((key, obj))
        for rule in self.types.get(key, ()):
            if rule in self.stack:
                for instance in self.stack[rule]:
                    if key in instance:
                        self.accept(instance, key, obj)
                        break
                else:
                    self.create(rule, key, obj)
            else:
                self.create(rule, key, obj)

class Key(object):
    def __init__(self, domain=None, entity=None, aspect=None):
        self.domain = domain
        self.entity = entity
        self.aspect = aspect

    RULE = re.compile("^((\w*):)?(\w*)(.(\w*))?$")
    @classmethod
    def create(cls, declaration):
        mo = cls.RULE.match(declaration)
        if mo is None:
            raise ValueError('Invalid declaration {0}'.format(declaration))
        _, domain, entity, _, aspect = mo.groups()
        return cls(domain=domain, entity=entity, aspect=aspect)

    def __repr__(self):
        declaration = self.entity
        if self.domain is not None:
            declaration = self.domain + ':' + declaration
        if self.aspect is not None:
            declaration += '.' + self.aspect
        return "<{0} {1}>".format(self.__class__.__name__, declaration)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, that):
        return (isinstance(that, Key) 
            and (self.domain is None or self.domain==that.domain)
            and self.entity==that.entity
            and self.aspect==that.aspect)

if __name__ == "__main__":
    scope = Scope('scope')

    from functools import partial
    import random

    def signal(*args):
        print '\t\tsignal fired', args

    actions = [
        partial(scope.add_key, Key(entity='Entity1', aspect='Aspect2'), 'Entity1-Aspect2'),
        partial(scope.add_key, Key(entity='Entity1'), 'Entity1'),
        partial(scope.add_key, Key(entity='Entity2'), 'Entity2'),
        partial(scope.add_key, Key(entity='Entity2', aspect='Aspect1'), 'Entity2-Aspect1'),
        partial(scope.add_key, Key(entity='Entity2', aspect='Aspect2'), 'Entity2-Aspect2'),
        partial(scope.add_key, Key(entity='Entity1', aspect='Aspect1'), 'Entity1-Aspect1'),
        partial(scope.add_rule, partial(signal, 'Coordinator1'), 'Entity1.Aspect1', 'Entity2.Aspect1'),
        partial(scope.add_rule, partial(signal, 'Coordinator2'), 'Entity1.Aspect1', 'Entity1.Aspect2'),
        partial(scope.add_rule, partial(signal, 'Coordinator3'), 'Entity2.Aspect1', 'Entity2.Aspect2'),
        partial(scope.add_rule, partial(signal, 'Coordinator4'), 'Entity1'),
        partial(scope.add_rule, partial(signal, 'Coordinator5'), 'Entity1.Aspect2', 'Entity2.Aspect2')
        ]
    
    print len(actions)
    indexes = range(len(actions))
    random.shuffle(indexes)
    print len(indexes)
    print indexes

    for index in indexes:
        action = actions[index]
        action()
