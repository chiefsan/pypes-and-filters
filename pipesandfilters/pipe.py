import abc
from multiprocessing import Pipe as mpPipe
from multiprocessing.connection import wait

from .pipestrategy import FIFO,LIFO

class BasePipe(object, metaclass=abc.ABCMeta):
    '''
    Parameters
    ----------
        incomingFilter : BaseFilter
            Filter from which pipe gets message.

        outgoingFilter : BaseFilter
            Filter to which pipe needs to send the message.
            
        strategy : PipeStrategy
            Strategy to reorder the messages present in pipe before sending to outgoingFilter (eg., FIFO,LIFO).
    '''
    @abc.abstractmethod
    def run(self):
        """
        Get messages from the incomingFilter,then apply the pipe strategy to it, and finally send them to the outgoingFilter.
        """
        raise NotImplementedError('to be implemented by children')

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

class Pipe(BasePipe):
    """A standard pipe.

    A pipe acts as a bridge to transfer message from one filter to another in Pipes and Filters architectural design pattern.
    """

    def run(self):
        while self._BasePipe__incomingConnection:
            inputs = []
            for reader in wait(self._BasePipe__incomingConnection):
                try:
                    input = reader.recv()
                    inputs.append(input)
                except EOFError:
                    self._BasePipe__incomingConnection.remove(reader)
                else:
                    print("Received input from Incoming Filter")

        # processing the input aggregate and choosing which element to send

        if self._BasePipe__strategy:
            inputs = self._BasePipe__strategy.transformMessageQueue(inputs)
        else:
            inputs = input
        self._BasePipe__inQueue[0].send(inputs)
        self._BasePipe__inQueue[0].close()

        while self._BasePipe__outQueue:
            for reader in wait(self._BasePipe__outQueue):
                try:
                    output = reader.recv()
                except EOFError:
                    self._BasePipe__outQueue.remove(reader)
                else:
                    print("Received output from inQueue")

        self._BasePipe__outgoingConnection[0].send(output)
        self._BasePipe__outgoingConnection[0].close()

    def setOutgoingFilter(self, outgoingFilter):
        """
        Set the outgoing filter of the pipe.

        Parameters
        ----------
            outgoingFilter : BaseFilter
        """
        self._BasePipe__outgoingFilter = outgoingFilter

    def getOutgoingFilter(self):
        """
        Get the outgoing filter of the pipe.

        Returns
        -------
            Filter
                The outgoing filter.
        """
        return self._BasePipe__outgoingFilter

    def setIncomingFilter(self, incomingFilter):
        """
        Set the filter from which the pipe receives the message.

        Parameters
        ----------
            incomingFilter : BaseFilter
                The incoming filter.
        """
        self._BasePipe__incomingFilter = incomingFilter

    def getIncomingFilter(self):
        """
        Get the incoming filter of the pipe.

        Returns
        -------
            Filter
                The incoming filter.
        """
        return self._BasePipe__incomingFilter

    def getId(self):
        """
        Get the id of the pipe.

        Returns
        -------
            str
                Pipe id
        """
        return self._BasePipe__id
