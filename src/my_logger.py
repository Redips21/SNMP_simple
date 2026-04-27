from typing import Protocol

class observer(Protocol):
    def update(self, info: str) -> None:
        pass


class My_logger:
    logs: list[str]
    observers: tuple[observer]

    def __init__(self, *observers):
        self.observers = observers
        self.logs = []

    def add_log(self, info: str):
        self.logs.append(info)
        self.notify(info)

    def notify(self, info):
        for observer in self.observers:
            observer.update(info)