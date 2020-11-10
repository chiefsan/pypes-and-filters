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
        self.__id = id
        self.__inQueue, self.__outQueue = mpPipe()
        self.__inQueue = [self.__inQueue]
        self.__outQueue = [self.__outQueue]
        self.__incomingFilter = incomingFilter
        self.__outgoingFilter = outgoingFilter
        reader, writer = mpPipe()
        self.__incomingFilter.addOutgoingConnection(writer)
        self.__incomingConnection = [reader]
        reader, writer = mpPipe()
        self.__outgoingFilter.addIncomingConnection(reader)
        self.__outgoingConnection = [writer]
        self.__incomingFilter.addOutgoingPipe(self)
        self.__outgoingFilter.addIncomingPipe(self)
        self.__strategy = strategy

    def run(self):
        """
        Gets message from the incomingFilter and apply strategy to it and sends to outgoingFilter
        """
        while self.__incomingConnection:
            inputs = []
            for reader in wait(self.__incomingConnection):
                try:
                    input = reader.recv()
                    inputs.append(input)
                except EOFError:
                    self.__incomingConnection.remove(reader)
                else:
                    print("Received input from Incoming Filter")

        # PROCESSING THE INPUT AND PICK WHICH INPUT TO SEND
        if self.__strategy:
            inputs = self.__strategy.transformMessageQueue(inputs)
        else:
            inputs = input
        self.__inQueue[0].send(inputs)
        self.__inQueue[0].close()

        while self.__outQueue:
            for reader in wait(self.__outQueue):
                try:
                    output = reader.recv()
                except EOFError:
                    self.__outQueue.remove(reader)
                else:
                    print("Received output from InQueue")

        self.__outgoingConnection[0].send(output)
        self.__outgoingConnection[0].close()

    def setOutgoingFilter(self, outgoingFilter):
        """
        Arguments:
            outgoingFilter(Filter) : sets the Filter to which pipe needs to send the message
        """
        self.__outgoingFilter = outgoingFilter

    def getOutgoingFilter(self):
        """
        Function to get the outgoingFilter
        """
        return self.__outgoingFilter

    def setIncomingFilter(self, incomingFilter):
        """
        Arguments:
            incomingFilter(Filter) : sets the Filter from which pipe receive the message
        """
        self.__incomingFilter = incomingFilter

    def getIncomingFilter(self):
        """
        Function to get the incomingFilter
        """
        return self.__incomingFilter

    def getId(self):
        """
        Function to get the id of the Pipe
        """
        return self.__id