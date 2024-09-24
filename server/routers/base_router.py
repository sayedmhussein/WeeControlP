from abc import ABC, abstractmethod

from fastapi import FastAPI

class BaseContext(ABC):
    def __init__(self, app: FastAPI, db):
        self.app = app
        self.db = db

    @abstractmethod
    def setup_routing(self):
        pass

    @abstractmethod
    async def setup_routing_async(self):
        pass
