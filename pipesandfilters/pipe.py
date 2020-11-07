import abc
from multiprocessing import Pipe as mpPipe
from multiprocessing.connection import wait

class BasePipe(object, metaclass=abc.ABCMeta):
    # Abstract class for pipes
    pass
    # @abc.abstractmethod
    # def receive(self):
    #     raise NotImplementedError('users must define receive to use this base class')
    # @abc.abstractclassmethod
    # def send(self,message):
    #     raise NotImplementedError('users must define send to use this base class')


class Pipe(BasePipe):
    def __init__(self, incomingFilter, outgoingFilter):
        self.InQueue,self.OutQueue = mpPipe()
        self.InQueue = [self.InQueue]
        self.OutQueue = [self.OutQueue]
        self.incomingFilter = incomingFilter
        self.outgoingFilter = outgoingFilter
        reader, writer = mpPipe()
        self.incomingFilter.addOutgoingConnection(writer)
        self.incomingConnection = [reader]
        reader, writer = mpPipe()
        self.outgoingFilter.addIncomingConnection(reader)
        self.outgoingConnection = [writer]
        self.incomingFilter.addOutgoingPipe(self)
        self.outgoingFilter.addIncomingPipe(self)

    def run(self):
        while self.incomingConnection:
            for r in wait(self.incomingConnection):
                try:
                    input = r.recv()
                except EOFError:
                    self.incomingConnection.remove(r)
                else:
                    print("Received input from Incoming Filter")

        # PROCESSING THE INPUT AND PICK WHICH INPUT TO SEND
        self.InQueue[0].send(input)
        self.InQueue[0].close()
        
        while self.OutQueue:
            for r in wait(self.OutQueue):
                try:
                    output = r.recv()
                except EOFError:
                    self.OutQueue.remove(r)
                else:
                    print("Received output from InQueue")
        
        self.outgoingConnection[0].send(input)
        self.outgoingConnection[0].close()

    def setOutgoingFilter(self, outgoingFilter):
        self.outgoingFilter = outgoingFilter

    def getOutgoingFilter(self):
        return self.outgoingFilter

    def setIncomingFilter(self, incomingFilter):
        self.incomingFilter = incomingFilter

    def getIncomingFilter(self):
        return self.incomingFilter
        