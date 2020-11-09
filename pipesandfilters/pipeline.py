import typing
from multiprocessing import Process
from .filter import Filter, SinkFilter, SourceFilter
from .pipe import Pipe
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


class Pipeline(object):

    """
    Pipeline class. 
    Encapsulates a set of data processing elements connected in series, where the output of one element is the input of the next one.
    """

    def __init__(self, id: str):
        """
        Parameters
        ----------
        id : str
            The name of the Pipeline.
        """
        self.id = id
        # Source Filter(starting point) of the pipeline
        self.sourceFilter = None
        # SinkFilter(ending point) of the Pipeline
        self.sinkFilter = []
        self.adjacency = {}
        self.components = []
        self.validated = False

    def setSourceFilter(self, sourceFilter: SourceFilter):
        """Set the SouceFilter for the Pipeline.
        Parameters
        ----------
        sourceFilter : SourceFilter.

        """
        self.sourceFilter = sourceFilter

    def addSinkFilter(self, sinkFilter: SinkFilter):
        """Append a Filter to the list of SinkFilter of the Pipeline.
        Parameters
        ----------
        sinkFilter : SinkFilter

        """
        self.sinkFilter.append(sinkFilter)

    def getSourceFilter(self):
        """Get the SourceFilter of the Pipeline.
        Returns
        -------
        SourceFilter
            The SourceFilter of the Pipeline
        """
        return self.sourceFilter

    def getSinkFilter(self):
        """Get the list of SinkFilter of the Pipeline.

        Returns
        -------
        SinkFilter[]
            The list of SinkFilter of the Pipeline.

        """
        return self.sinkFilter

    def validate(self):
        """Validate the Pipeline.
        
        Verify whether the Pipeline can be represented by an acyclic connected graph with appropriate filters at the leaf nodes. Breadth First Search is applied on the Pipeline.
       
        Returns
        -------
        Bool
            A boolean value that indicates whether the Pipeline is valid or not.

        """

        def add_edge(head, tail, weight):
            """
            Adds an edge to the graph.
            `head` and `tail are vertices representing the endpoints of the edge
            `weight` is the weight of the egde from head to tail
            """
            # Add the vertices to the graph (if they haven't already been added)
            add_vertex(head)
            add_vertex(tail)

            # Self edge => invalid
            if head == tail:
                return

            # Since graph is directed, we are not adding the reverse edge
            self.adjacency[head][tail] = weight

        def add_vertex(vertex):
            """
            Adds a vertex to the graph.
            `vertex` must be a hashable object
            """
            if vertex not in self.adjacency:
                self.adjacency[vertex] = {}

        # Create a dictionary to maintain the list of Filters visited by the BFS.
        visited = defaultdict(bool)

        # Queue to store the filters
        queue = []

        # Enqueue the sourceFilter
        queue.append(self.getSourceFilter())

        while queue:
            print(queue, self.components)

            # Dequeue the currentFilter to process
            currentFilter = queue.pop(0)

            # Add the filter to the list of components
            self.components.append(currentFilter)

            # Mark the currentFilter as visited
            visited[currentFilter] = True

            # Reached a leaf node. Continue with the next iteration.
            if isinstance(currentFilter, SinkFilter):
                continue
            if len(currentFilter.getOutgoingPipes()) == 0:
                # NonSink filter is a leaf node => infeasible.
                return False

            # Get all outgoing pipes of curerentFilter.
            for pipe in currentFilter.getOutgoingPipes():

                # Add the pipe to the list of components
                self.components.append(pipe)

                # If a connected Filter has not been visited, then mark it visited and enqueue it
                if visited[pipe.getOutgoingFilter()] != True:
                    queue.append(pipe.getOutgoingFilter())
                    add_edge(currentFilter, pipe.getOutgoingFilter(), 1)
                else:
                    print("Not Feasible")
                    # Pipeline is cyclic => infeasible
                    return False

        self.validated = True
        return True

    def run(self, input):
        """Fire up all the components in the pipeline.
        Parameters
        ----------
        input
        
        Returns
        -------
        output
        """

        # Validate the pipeline if necessary
        if not self.validated:
            self.validate()

        index = 0
        for component in self.components:
            index += 1
            if isinstance(component, SourceFilter):
                component.run(input)
            else:
                output = component.run()
        print(output)

    def visualize(self, path):
        """
        Visualize the Pipeline using [networkx](https://pypi.org/project/networkx/).

        Parameters
        ----------
        path : file path
            absolute path to store an image of the Pipeline
        """
        graph = nx.Graph()

        # add edges to the graph
        for head in self.adjacency:
            for tail in self.adjacency[head]:
                weight = self.adjacency[head][tail]
                graph.add_edge(head, tail, weight=weight)

        # generate a layout for the graph and set the vertex labels to the Filter ids
        layout = nx.spring_layout(graph, seed=0)
        labels = {v: v.id for v in graph.nodes()}
        nx.draw(
            graph,
            layout,
            node_size=0,
            labels=labels,
            with_labels=True,
            bbox=dict(facecolor="skyblue", edgecolor="black", boxstyle="round,pad=0.2"),
        )

        # set the edge labels to the Pipe ids
        labels = {e: e[1].getIncomingPipes()[0].id for e in graph.edges()}
        nx.draw_networkx_edge_labels(graph, pos=layout, edge_labels=labels)

        # save the figure in the given path
        plt.savefig(path)
