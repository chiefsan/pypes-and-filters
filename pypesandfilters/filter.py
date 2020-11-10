import abc
import typing
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait
from .pipe import Pipe
from .message import Message


class BaseFilter(object, metaclass=abc.ABCMeta):
    """
    Abstract base filter class.
    
    Receives messages and preforms required processing on them before sending them to appropriate destinations.
    """

    @abc.abstractmethod
    def run(self):
        """Abstract method that determines how the filter executes the required process when spawned. 

        It is responsible for receiving messages from incoming pipes, if any, and sending messages to outgoing pipes, if any.
        """
        raise NotImplementedError("children should implement")

    @abc.abstractmethod
    def __init__(self, id: str, filterProcess):
        """

        Parameters
        ----------
            id : str
                Identifier for the filter. 
                
            filterProcess : function
                The calllable object (function) that is applied by the filter on the message.
        """
        raise NotImplementedError("children should implement")

    def process(self, data):
        """Apply `filterProcess` on the message.
        
        Parameters
        ----------
            data : object
                The object on which `filterProcess` is applied.
        """
        output = self.__filterProcess(data)
        return output
    
    def getId(self):
        """
        Get the id of the filter.

        Returns
        -------
            str
                The id of the filter.
        """
        return self.__id


class Filter(BaseFilter):
    """A standard filter. 
    
    A component in the pipeline that has both incoming and outgoing pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.__outgoingPipes = []
        self.__incomingPipes = []
        self.__incomingConnections = []
        self.__outgoingConnections = []
        self._BaseFilter__filterProcess = filterProcess
        self.__id = id

    def addOutgoingPipe(self, pipe: Pipe):
        """ Add an outgoing pipe to the filter.

        Parameters
        ----------
            pipe : Pipe
                The pipe connected to the outgoing end of the filter.
        """
        self.__outgoingPipes.append(pipe)

    def getOutgoingPipes(self):
        """ Get outgoing pipes of the filter.

        Returns
        -------
            Pipe[]
                The pipes at the outgoing end of the filter.
        """
        return self.__outgoingPipes

    def getIncomingPipes(self):
        """ Get incoming pipes of the filter.

        Returns
        -------
            Pipe[]
                The pipes at the incoming end of the filter.
        """
        return self.__incomingPipes

    def addIncomingPipe(self, pipe: Pipe):
        """ Add an incoming pipe to the filter.

        Parameters
        ----------
            pipe : Pipe
                The pipe connected to the incoming end of the filterss.
        """
        self.__incomingPipes.append(pipe)

    def getIncomingConnections(self):
        """ Get incoming connection objects of the filter.

        Returns
        -------
            Connection[]
                The connections at the incoming end of the filter.
        """
        return self.__incomingConnections

    def addIncomingConnection(self, incomingConnection):
        """ Add an incoming connection object to the filter.

        Parameters
        ----------
            incomingConnection : Connection
                The connection object at the incoming end of the filter.
        """
        self.__incomingConnections.append(incomingConnection)

    def getOutgoingConnections(self):
        """ Get outgoing connection objects of the filter.

        Returns
        -------
            Connection[]
                The connections at the outgoing end of the filter.
        """
        return self.__outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        """ Add an outgoing connection object to the filter.

        Parameters
        ----------
            outgoingConnection : Connection
                The connection object at the outgoing end of the filter.
        """
        self.__outgoingConnections.append(outgoingConnection)

    def run(self):
        while self.__incomingConnections:
            for reader in wait(self.__incomingConnections):
                try:
                    input = reader.recv()
                except EOFError:
                    self.__incomingConnections.remove(reader)
                else:
                    print("Received")
        output = self.process(input)
        for conn in self.__outgoingConnections:
            conn.send(output)
            conn.close()


class SourceFilter(BaseFilter):
    """
    A source filter. 
    
    A component in the pipeline that has outgoing pipes but no incoming pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.__outgoingPipes = []
        self.__outgoingConnections = []
        self._BaseFilter__filterProcess = filterProcess
        self.__id = id

    def getOutgoingPipes(self):
        """ Get outgoing pipes of the filter.

        Returns
        -------
            Pipe[]
                The pipes at the outgoing end of the filter.
        """
        return self.__outgoingPipes

    def addOutgoingPipe(self, pipe: Pipe):
        """ Add an outgoing pipe to the filter.

        Parameters
        ----------
            pipe : Pipe
                The pipe connected to the outgoing end of the filter.
        """
        self.__outgoingPipes.append(pipe)

    def getOutgoingConnections(self):
        """ Get outgoing connection objects of the filter.

        Returns
        -------
            Connection[]
                The connections at the outgoing end of the filter.
        """
        return self.__outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        """ Add an outgoing connection object to the filter.
        
        Parameters
        ----------
            outgoingConnection : Connection
                The connection object at the outgoing end of the filter.
        """
        self.__outgoingConnections.append(outgoingConnection)

    def run(self, input):
        output = self.process(input)
        for conn in self.__outgoingConnections:
            conn.send(output)
            conn.close()


class SinkFilter(BaseFilter):
    """
    A sink filter. 

    A component in the pipeline that has incoming pipes but no outgoing pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.__incomingPipes = []
        self.__incomingConnections = []
        self._BaseFilter__filterProcess = filterProcess
        self.__id = id

    def addIncomingPipe(self, pipe: Pipe):
        """ Add an incoming pipe to the filter.
        
        Parameters
        ----------
            pipe : Pipe
                The pipe connected to the incoming end of the filter.
        """
        self.__incomingPipes.append(pipe)

    def getIncomingPipes(self):
        """ Get incoming pipes of the filter.
        
        Returns
        -------
            Pipe[]
                The pipes at the incoming end of the filter.
        """
        return self.__incomingPipes

    def getIncomingConnections(self):
        """ Get incoming connection objects of the filter.
        
        Returns
        -------
            Connection[]
                The connections at the incoming end of the filter.
        """
        return self.__incomingConnections

    def addIncomingConnection(self, incomingConnection):
        """ Add an incoming connection object to the filter.
        
        Parameters
        ----------
            incomingConnection : Connection
                The connection object at the incoming end of the filter.
        """
        self.__incomingConnections.append(incomingConnection)

    def run(self):
        print(len(self.__incomingConnections))
        if len(self.__incomingConnections) == 0:
            print("No incoming connections yet!")
        while self.__incomingConnections:
            for reader in wait(self.__incomingConnections):
                try:
                    input = reader.recv()
                except EOFError:
                    self.__incomingConnections.remove(reader)
                else:
                    print("Received")
        output = self.process(input)
        print(output)
        return output
