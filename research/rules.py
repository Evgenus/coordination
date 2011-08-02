from collections import defaultdict

class Rule(object):
    def __init__(self):
        self.left = set(self.parts)

    def add(self, part):
        self.left.remove(part)
        if self.left:
            return False
        self()
        return True

    def __call__(self):
        print 'rule {0} activated'.format(self.__class__.__name__)

    def __contains__(self, part):
        return part in self.left

    def __repr__(self):
        return "<{0} {1} of {2}>".format(
            self.__class__.__name__,
            self.left, self.parts)

class Scope(object):
    def __init__(self):
        self.types = defaultdict(list)
        self.stack = defaultdict(list)

    def add_rule(self, rule):
        for part in rule.parts:
            self.types[part].append(rule)

    def create(self, rule, part):
        instance = rule()
        self.stack[rule].append(instance)
        instance.add(part)

    def accept(self, instance, part):
        if instance.add(part):
            self.stack[type(instance)].remove(instance)

    def add(self, part):
        for rule in self.types.get(part, ()):
            if rule in self.stack:
                for instance in self.stack[rule]:
                    if part in instance:
                        self.accept(instance, part)
                        break
                else:
                    self.create(rule, part)
            else:
                self.create(rule, part)

class Rule1(Rule):
    parts = set((
        ('Entity1', 'Aspect1'), 
        ('Entity2', 'Aspect1'), 
        ))

class Rule2(Rule):
    parts = set((
        ('Entity1', 'Aspect1'), 
        ('Entity1', 'Aspect2'), 
        ))

class Rule3(Rule):
    parts = set((
        ('Entity2', 'Aspect1'), 
        ('Entity2', 'Aspect2'), 
        ))

if __name__ == "__main__":
    scope = Scope()

    scope.add_rule(Rule1)
    scope.add_rule(Rule2)
    scope.add_rule(Rule3)

    seq = [
        ('Entity1', 'Aspect1'),
        ('Entity1', 'Aspect2'),
        ('Entity1',),
        ('Entity2', 'Aspect1'),
        ('Entity2', 'Aspect2'),
        ('Entity2',),
        ]

    for part in seq:
        print part
        scope.add(part)
