import abc
import typing
from multiprocessing import Process

class Pipeline(object, metaclass=abc.ABCMeta):
    '''
    Abstract base Pipeline class which receives a message and preforms required processing.
    '''
    def __init__(self, id: str):
        self.id = id
    