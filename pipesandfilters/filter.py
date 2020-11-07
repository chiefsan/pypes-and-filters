import abc
import typing
from multiprocessing import Process
from .pipe import Pipe
from .message import Message


class BaseFilter(object, metaclass=abc.ABCMeta):
    '''
    Abstract base Filter class which receives a message and preforms required processing.
    '''    
    def receive(self):
        raise NotImplementedError('not nececssary at the moment')

    def send(self):
        raise NotImplementedError('not nececssary at the moment')

    def __init__(self, id: str, filterProcess):
        self.id = id
        self.filterProcess = filterProcess
    
    def process(self, data):
        output = filterProcess(data)


class Filter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.incomingPipes = []
        self.incomingConnection = {}
        self.outgoingConnection = {}
    
    def addOutgoingPipe(self, pipe: Pipe):
        self.outgoingPipes.append(pipe)
    
    def addIncomingPipe(self, pipe: Pipe):
        self.incomingPipes.append(pipe)

    def run():
        while incomingConnections:
            for r in wait(incomingConnections):
                try:
                    input = r.recv()
                except EOFError:
                    incomingConnections.remove(r)
                else:
                    print("Received")
        output = process(input)
        for conn in outgoingConnections:
            conn.send(output)

class SourceFilter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.outgoingConnections = []

    def getOutgoingPipes(self):
        return self.outgoingPipes

    def addOutgoingPipe(self, pipe: Pipe):
        self.outgoingPipes.append(pipe)
    
    def getOutgoingConnections(self):
        return self.outgoingConnections

    def setOutgoingConnections(self, outgoingConnections):
        self.outgoingConnections = outgoingConnections

    def run(input):
        output = process(input)
        for conn in outgoingConnections:
            conn.send(output)
    

class SinkFilter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.incomingPipes = []
        self.incomingConnections = []

    def addIncomingPipe(self, pipe: Pipe):
        self.incomingPipes.append(pipe)
    
    def getIncomingPipes(self):
        return self.incomingPipes

    def getIncomingConnections(self):
        return self.incomingConnections

    def setIncomingConnections(self, incomingConnections):
        self.incomingConnections = incomingConnections

    def run():
        while incomingConnections:
            for r in wait(incomingConnections):
                try:
                    input = r.recv()
                except EOFError:
                    incomingConnections.remove(r)
                else:
                    print("Received")
        output = process(input)
        return output
