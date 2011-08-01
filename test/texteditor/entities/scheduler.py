#external
from coordination.wire import Entity, Aspect
from coordination.runtime import MessageQueue

__all__ = ["Scheduler"]

class Scheduler(Entity):
    
    class Queue(Aspect, MessageQueue):
        pass