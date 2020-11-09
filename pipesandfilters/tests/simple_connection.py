from pipesandfilters import Filter, SourceFilter, SinkFilter

sink = SinkFilter(1, abs)
source = SourceFilter(1, abs)
from multiprocessing import Pipe

reader, writer = Pipe()
sink.setIncomingConnections([reader])
source.setOutgoingConnections([writer])
source.run(24)
sink.run()
