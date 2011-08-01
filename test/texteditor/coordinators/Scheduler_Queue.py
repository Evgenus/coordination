#external
from coordination.wire import Coordinator
from coordination.runtime import Action

__all__ = [
    "Coordinator_Scheduler_Queue"
    ]

class Coordinator_Scheduler_Queue(Coordinator):
    require = [
        ('Scheduler', 'Queue'),
        ]
    def __init__(self, aspect_queue):
        self.aspect_queue = aspect_queue

    def create(self):
        # Dependency Injection
        Action.scheduler = self.aspect_queue
