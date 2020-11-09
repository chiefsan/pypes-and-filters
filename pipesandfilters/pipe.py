import abc
from multiprocessing import Pipe as mpPipe
from multiprocessing.connection import wait

# from pipestrategy import FIFO,LIFO


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
    """Implements Pipe concept
    Pipe acts as a bridge to transfer message from one filter to another in Pipes and Filter architectural design pattern.
    Arguments:
        incomingFilter(Filter) : Filter from which pipe gets message
        outgoingFilter(Filter) : Filter to which pipe needs to send the message
        strategy(PipeStrategy) : Strategy to reorder the messages present in pipe before sending to outgoingFilter (eg., FIFO,LIFO)
    """

    def __init__(self, id, incomingFilter, outgoingFilter, strategy=None):
        self.id = id
        self.InQueue, self.OutQueue = mpPipe()
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
        self.strategy = strategy

    def run(self):
        """
        Gets message from the incomingFilter and apply strategy to it and sends to outgoingFilter
        """
        while self.incomingConnection:
            Inputs = []
            for r in wait(self.incomingConnection):
                try:
                    input = r.recv()
                    Inputs.append(input)
                except EOFError:
                    self.incomingConnection.remove(r)
                else:
                    print("Received input from Incoming Filter")

        # PROCESSING THE INPUT AND PICK WHICH INPUT TO SEND
        if self.strategy:
            Inputs = self.strategy.transformMessageQueue(Inputs)
        else:
            Inputs = input
        self.InQueue[0].send(Inputs)
        self.InQueue[0].close()

        while self.OutQueue:
            for r in wait(self.OutQueue):
                try:
                    output = r.recv()
                except EOFError:
                    self.OutQueue.remove(r)
                else:
                    print("Received output from InQueue")

        self.outgoingConnection[0].send(output)
        self.outgoingConnection[0].close()

    def setOutgoingFilter(self, outgoingFilter):
        """
        Arguments:
            outgoingFilter(Filter) : sets the Filter to which pipe needs to send the message
        """
        self.outgoingFilter = outgoingFilter

    def getOutgoingFilter(self):
        """
        Function to get the outgoingFilter
        """
        return self.outgoingFilter

    def setIncomingFilter(self, incomingFilter):
        """
        Arguments:
            incomingFilter(Filter) : sets the Filter from which pipe receive the message
        """
        self.incomingFilter = incomingFilter

    def getIncomingFilter(self):
        """
        Function to get the incomingFilter
        """
        return self.incomingFilter
