#external
from coordination.wire import Coordinator

__all__ = [
    "Coordinator_Reactor_Gtk_Scheduler_Queue"
    ]

class Coordinator_Reactor_Gtk_Scheduler_Queue(Coordinator):
    require = [
        ('Reactor', 'Gtk'),
        ('Scheduler', 'Queue'),
        ]
    def __init__(self, aspect_reactor, aspect_queue):
        self.aspect_reactor = aspect_reactor
        self.aspect_queue = aspect_queue

    def create(self):
        self.aspect_reactor.set_callback(self.aspect_queue)

