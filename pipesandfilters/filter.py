import abc
import typing
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait
from .pipe import Pipe
from .message import Message


class BaseFilter(object, metaclass=abc.ABCMeta):
    """
    Abstract base Filter class.
    
    Receives messages and preforms required processing on them before sending them to appropriate destinations.
    """

    @abc.abstractmethod
    def run(self):
        """Abstract method that determines how the Filter executes the required process when spawned. 

        It is responsible for receiving messages from incoming pipes, if any, and sending messages to outgoing pipes, if any.
        """
        raise NotImplementedError("not nececssary at the moment")

    def __init__(self, id: str, filterProcess):
        """Determine how the Filter executes the required process when spawned.
        Parameters
        ----------
        id : str
            Identifier for the Filter. 
        filterProcess : Filter
            The calllable object (function) that is applied by the Filter on the message.
        """
        pass

    def process(self, data):
        """Apply `filterProcess` on the message.
        Parameters
        ----------
        data : object
            The object on which `filterProcess` is applied.
        """
        output = self.filterProcess(data)
        return output


class Filter(BaseFilter):
    """A Standard Filter. 
    
    A component in the pipeline that has both incoming and outgoing pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.incomingPipes = []
        self.incomingConnections = []
        self.outgoingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def addOutgoingPipe(self, pipe: Pipe):
        """ Add an outgoing pipe to the Filter.
        Parameters
        ----------
        pipe : Pipe
            The pipe connected to the outgoing end of the Filter.
        """
        self.outgoingPipes.append(pipe)

    def getOutgoingPipes(self):
        """ Return outgoing pipes of the Filter.
        Returns
        -------
        Pipe[]
            The pipes at the outgoing end of the Filter.
        """
        return self.outgoingPipes

    def getIncomingPipes(self):
        """ Return incoming pipes of the Filter.
        Returns
        -------
        Pipe[]
            The pipes at the incoming end of the Filter.
        """
        return self.incomingPipes

    def addIncomingPipe(self, pipe: Pipe):
        """ Add an incoming pipe to the Filter.
        Parameters
        ----------
        pipe : Pipe
            The pipe connected to the incoming end of the Filter.
        """
        self.incomingPipes.append(pipe)

    def getIncomingConnections(self):
        """ Return incoming connection objects of the Filter.
        Returns
        -------
        Connection[]
            The connections at the incoming end of the Filter.
        """
        return self.incomingConnections

    def addIncomingConnection(self, incomingConnection):
        """ Add an incoming connection object to the Filter.
        Parameters
        ----------
        incomingConnection : Connection
            The connection object at the incoming end of the Filter.
        """
        self.incomingConnections.append(incomingConnection)

    def getOutgoingConnections(self):
        """ Return outgoing connection objects of the Filter.
        Returns
        -------
        Connection[]
            The connections at the outgoing end of the Filter.
        """
        return self.outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        """ Add an outgoing connection object to the Filter.
        Parameters
        ----------
        outgoingConnection : Connection
            The connection object at the outgoing end of the Filter.
        """
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
    """
    A Source Filter. 
    
    A component in the pipeline that has outgoing pipes but no incoming pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.outgoingPipes = []
        self.outgoingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def getOutgoingPipes(self):
        """ Return outgoing pipes of the Filter.
        Returns
        -------
        Pipe[]
            The pipes at the outgoing end of the Filter.
        """
        return self.outgoingPipes

    def addOutgoingPipe(self, pipe: Pipe):
        """ Add an outgoing pipe to the Filter.
        Parameters
        ----------
        pipe : Pipe
            The pipe connected to the outgoing end of the Filter.
        """
        self.outgoingPipes.append(pipe)

    def getOutgoingConnections(self):
        """ Return outgoing connection objects of the Filter.
        Returns
        -------
        Connection[]
            The connections at the outgoing end of the Filter.
        """
        return self.outgoingConnections

    def addOutgoingConnection(self, outgoingConnection):
        """ Add an outgoing connection object to the Filter.
        Parameters
        ----------
        outgoingConnection : Connection
            The connection object at the outgoing end of the Filter.
        """
        self.outgoingConnections.append(outgoingConnection)

    def run(self, input):
        output = self.process(input)
        for conn in self.outgoingConnections:
            conn.send(output)
            conn.close()


class SinkFilter(BaseFilter):
    """
    A Sink Filter. 
    A component in the pipeline that has incoming pipes but no outgoing pipes.
    """

    def __init__(self, id: str, filterProcess):
        self.incomingPipes = []
        self.incomingConnections = []
        self.filterProcess = filterProcess
        self.id = id

    def addIncomingPipe(self, pipe: Pipe):
        """ Add an incoming pipe to the Filter.
        Parameters
        ----------
        pipe : Pipe
            The pipe connected to the incoming end of the Filter.
        """
        self.incomingPipes.append(pipe)

    def getIncomingPipes(self):
        """ Return incoming pipes of the Filter.
        Returns
        -------
        Pipe[]
            The pipes at the incoming end of the Filter.
        """
        return self.incomingPipes

    def getIncomingConnections(self):
        """ Return incoming connection objects of the Filter.
        Returns
        -------
        Connection[]
            The connections at the incoming end of the Filter.
        """
        return self.incomingConnections

    def addIncomingConnection(self, incomingConnection):
        """ Add an incoming connection object to the Filter.
        Parameters
        ----------
        incomingConnection : Connection
            The connection object at the incoming end of the Filter.
        """
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
