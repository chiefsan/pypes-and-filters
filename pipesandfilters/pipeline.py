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
        """
        Parameters
        ----------
        id : str
            The name of the Pipeline
        """
        self.id= id
        #Source Filter(starting point) of the pipeline
        self.sourceFilter = None
        #SinkFilter(ending point) of the Pipeline 
        self.sinkFilter = []

    def setSourceFilter(self, sourcefilter:Filter):
        """Set the SouceFilter for the Pipeline
        Parameters
        ----------
        sourcefilter : Filter

        """
        self.source = sourcefill
    def addSinkFilter(self, sinkfilter:Filter):
        """Append a Filter to the SinkFilter list of the Pipeline
        Parameters
        ----------
        sinkfilter : Filter

        """
        self.sinkFilter.append(sinkfilter)
    def getSourceFilter(self):
        """ Get SourceFilter of the Pipeline
        Parameters
        ----------
       
        Returns
        -------
        Filter
            
            a Filter representing the SinkFilter

        """
        return self.sourceFilter 
    def getSinkFilter(self):
        """Get SinkFilters of the Pipeline
        Parameters
        ----------
       
        Returns
        -------
        List
            
            a list Filter representing the SinkFilter

        """
        return self.sinkFilter
    
    def validategraph(self):
        """validating the Pipeline whether there are any cycles or not
        Parameters
        ----------
       
        Returns
        -------
        Bool
            
            a bool value to show the Pipeline is Feasible or not

        """
        # Visited dictionary to store the Filters visited condition 
        visited = defaultdict(bool)
        # Queue to store the filters
        queue = [] 
        # Enqueue the sourceFilter
        queue.append(self.getSourceFilter())
  
        while queue: 
            # Dequeue the currentFilter to process
            currentFilter = queue.pop(0) 
            # Mark the currentFilter as visited 
            visited[currentfilter] = True
            # Get all connected Filters of the curerentFilter.  
            for pipe in currentFilter.getOutgoingPipes(): 
                # If a connected Filter has not been visited, then mark it visited and enqueue it
                if visited[pipe.getOutgoingFilter]!=True and isinstance(pipe.getOutgoingFilter(),sinkFilter): 
                    queue.append(pi.getOutgoingFilter())
                else:
                    print("Not Feasible")
                    #Cycle occurs and the Pipeline is notFeasible
                    return False
        #Cycle occurs and the Pipeline is notFeasible
        return True           
                
