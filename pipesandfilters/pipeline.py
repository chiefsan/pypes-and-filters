import abc
import typing
from multiprocessing import Process
from .filter import Filter
from .pipe import Pipes

class Pipeline(object, metaclass=abc.ABCMeta):

    '''
    Abstract base Pipeline class which receives a message and preforms required processing.
    '''
    def __init__(self, id: str):
        self.id= ""
        self.source = None
        self.sink = None
        self.connections=dict()
        self.filters=[]
    
    def setSourceFilter(self, sourcefill:Filter):
        self.source = sourcefill
    def setSinkFilter(self, sinkfil:Filter):
        self.sink = sinkfil
    def getSourceFilter(self):
        return self.source 
    def getsinkFilter(self):
        return self.sink
    def addfilter(self,beforefilter:Filter, currentfilter:Filter):
        if(beforefilter not in self.filters):
            self.filters.append(beforefilter)
        if(currentfilter not in self.filters):
            self.filters.append(currentfilter)
        if beforefilter not in self.connections:
            self.connections[beforefilter.id] = [currentfilter.id]
        else:
            self.connections[beforefilter.id].append(currentfilter.id)
    def connect(self):
        for i in self.connections:
            for k in self.filters:
                if(i==k.id):
                    outpipes = k.outgoingpipes
            for j in self.connections[i]:
                for k in self.filters:
                    if(j==k.id):
                        k.incomingpipes = outpipes 
                        
                
                
