from pipesandfilters import Filter, SourceFilter, SinkFilter
sink = SinkFilter(1,abs)
filter = Filter(1, abs)
source = SourceFilter(1, abs)
from multiprocessing import Pipe
reader,writer = Pipe()
source.setOutgoingConnections([writer])
filter.setIncomingConnections([reader])

reader,writer = Pipe()
filter.setOutgoingConnections([writer])
sink.setIncomingConnections([reader])
source.run(24)
filter.run()
sink.run()