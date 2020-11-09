import abc
import typing
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait
from .pipe import Pipe
from .message import Message


class BaseFilter(object, metaclass=abc.ABCMeta):
    """
    Abstract base Filter class which receives a message and preforms required processing.
    """

    def receive(self):
        raise NotImplementedError("not nececssary at the moment")

    def send(self):
        raise NotImplementedError("not nececssary at the moment")

    def __init__(self, id: str, filterProcess):
        pass

    def process(self, data):
        output = self.filterProcess(data)
        return output


class Filter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.incomingPipes = []
        self.incomingConnections = []
        self.outgoingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def addOutgoingPipe(self, pipe: Pipe):
        self.outgoingPipes.append(pipe)

    def addIncomingPipe(self, pipe: Pipe):
        self.incomingPipes.append(pipe)

    def getIncomingConnections(self):
        return self.incomingConnections

    def addIncomingConnection(self, incomingConnection):
        self.incomingConnections.append(incomingConnection)

    def getOutgoingConnections(self):
        return self.outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        self.outgoingConnections.append(outgoingConnection)

    def run(self):
        while self.incomingConnections:
            for r in wait(self.incomingConnections):
                try:
                    input = r.recv()
                except EOFError:
                    self.incomingConnections.remove(r)
                else:
                    print("Received")
        output = self.process(input)
        for conn in self.outgoingConnections:
            conn.send(output)
            conn.close()


class SourceFilter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.outgoingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def getOutgoingPipes(self):
        return self.outgoingPipes

    def addOutgoingPipe(self, pipe: Pipe):
        self.outgoingPipes.append(pipe)

    def getOutgoingConnections(self):
        return self.outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        self.outgoingConnections.append(outgoingConnection)

    def run(self, input):
        output = self.process(input)
        for conn in self.outgoingConnections:
            conn.send(output)
            conn.close()


class SinkFilter(BaseFilter):
    def __init__(self, id: str, filterProcess):
        self.incomingPipes = []
        self.incomingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def addIncomingPipe(self, pipe: Pipe):
        self.incomingPipes.append(pipe)

    def getIncomingPipes(self):
        return self.incomingPipes

    def getIncomingConnections(self):
        return self.incomingConnections

    def addIncomingConnection(self, incomingConnection):
        self.incomingConnections.append(incomingConnection)

    def run(self):
        print(len(self.incomingConnections))
        if len(self.incomingConnections) == 0:
            print("No incoming connections yet!")
        while self.incomingConnections:
            for r in wait(self.incomingConnections):
                try:
                    input = r.recv()
                except EOFError:
                    self.incomingConnections.remove(r)
                else:
                    print("Received")
        output = self.process(input)
        print(output)
        return output
