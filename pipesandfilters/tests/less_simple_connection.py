from pipesandfilters import Filter, SourceFilter, SinkFilter, Pipe, Pipeline

sink = SinkFilter("sink", abs)
filter = Filter(1, abs)
source = SourceFilter("source", abs)
p = Pipe("pipe", source, sink)
pipeline = Pipeline("lol")
pipeline.setSourceFilter(source)
pipeline.addSinkFilter(sink)
# pipeline.validate()
# pipeline.myGraphViz("/mnt/c/Users/sanja/Desktop/lol.PNG")
pipeline.run(2)
