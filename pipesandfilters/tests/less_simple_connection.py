from pipesandfilters import Filter, SourceFilter, SinkFilter, Pipe
sink = SinkFilter(1,abs)
filter = Filter(1, abs)
source = SourceFilter(1, abs)
p = Pipe(source, sink)
source.run()
p.run()
sink.run()
