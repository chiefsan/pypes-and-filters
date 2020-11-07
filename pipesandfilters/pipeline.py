import abc
import typing
from multiprocessing import Process
from .filter import Filter
from .pipe import Pipe

class Pipeline(object, metaclass=abc.ABCMeta):

    '''
    Abstract base Pipeline class which receives a message and preforms required processing.
    '''
    def __init__(self, id: str):
        self.id= id
        self.source = None
        self.sink = []
        
    def setSourceFilter(self, sourcefill:Filter):
        self.source = sourcefill
    def setSinkFilter(self, sinkfil:Filter):
        self.sink = sinkfil
    def getSourceFilter(self):
        return self.source 
    def getSinkFilter(self):
        return self.sink
    def validategraph(self):
        visited = [] 
        queue = [] 

        queue.append(self.getSourceFilter())
  
        while queue: 
            f = queue.pop(0) 
            visited.append(f)
            for pi in f.getOutgoingPipes(): 
                if pi.getOutgoingFilter() not in visited and pi.getOutgoingFilter() not in self.getSinkFilter(): 
                    queue.append(pi.getOutgoingFilter())
                else:
                    print("Not Feasible")
                    return
    def start(self):
        print("Start")                
                
