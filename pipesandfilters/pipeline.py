import abc
import typing
from multiprocessing import Process
from .filter import Filter, SinkFilter
from .pipe import Pipe
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


class Pipeline(object, metaclass=abc.ABCMeta):

    """
    Abstract base Pipeline class which receives a message and preforms required processing.
    """

    def __init__(self, id: str):
        """
        Parameters
        ----------
        id : str
            The name of the Pipeline
        """
        self.id = id
        # Source Filter(starting point) of the pipeline
        self.sourceFilter = None
        # SinkFilter(ending point) of the Pipeline
        self.sinkFilter = []
        self.adjacency = {}
        self.components = []

    def setSourceFilter(self, sourcefilter: Filter):
        """Set the SouceFilter for the Pipeline
        Parameters
        ----------
        sourcefilter : Filter

        """
        self.sourceFilter = sourcefilter

    def addSinkFilter(self, sinkfilter: Filter):
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

    def validate(self):
        """validating the Pipeline whether there are any cycles or not
        Parameters
        ----------
       
        Returns
        -------
        Bool
            
            a bool value to show the Pipeline is Feasible or not

        """

        def add_edge(self, head, tail, weight):
            """
            Adds an edge to the graph.
            `head` and `tail are vertices representing the endpoints of the edge
            `weight` is the weight of the egde from head to tail
            """
            # Add the vertices to the graph (if they haven't already been added)
            self.add_vertex(head)
            self.add_vertex(tail)

            # Self edge => invalid
            if head == tail:
                return

            # Since graph is undirected, add both edge and reverse edge
            self.adjacency[head][tail] = weight

            self.adjacency[tail][head] = weight

        def add_vertex(self, vertex):
            """
            Adds a vertex to the graph.
            `vertex` must be a hashable object
            """
            if vertex not in self.adjacency:
                self.adjacency[vertex] = {}
                self.num_vertices += 1

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
            self.components.append(currentFilter)
            visited[currentFilter] = True
            if isinstance(currentFilter, SinkFilter):
                continue
            # Get all connected Filters of the curerentFilter.
            for pipe in currentFilter.getOutgoingPipes():
                self.components.append(pipe)
                # If a connected Filter has not been visited, then mark it visited and enqueue it
                if visited[pipe.getOutgoingFilter] != True:
                    queue.append(pipe.getOutgoingFilter())
                else:
                    print("Not Feasible")
                    # Cycle occurs and the Pipeline is notFeasible
                    return False
        # Cycle occurs and the Pipeline is notFeasible
        return True

    def run(self, input):
        lol = 0
        for i in self.components:
            lol += 1
            print(i, type(i), lol)
            if lol == 1:
                i.run(input)
            else:
                output = i.run()
        print(output)

    def myGraphViz(self):
        """
        Visualizes the graph using [networkx](https://pypi.org/project/networkx/).
        """
        G = nx.Graph()
        for head in self.adjacency:
            for tail in self.adjacency[head]:
                weight = self.adjacency[head][tail]
                G.add_edge(head, tail, weight=weight)
        layout = nx.spring_layout(G, seed=0)
        nx.draw(G, layout, with_labels=True)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        plt.show()
