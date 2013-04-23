from ladspam_pb2 import *

# Returns the index of the added plugin
def add_plugin(synth, label):
	plugin = synth.plugins.add()
	plugin.label = label
	return len(synth.plugins) - 1

def make_connection(synth, source_index, source_port_index, sink_index, sink_port_index):
	connection = synth.connections.add()
	connection.source_index = source_index
	connection.source_port_index = source_port_index
	connection.sink_index = sink_index
	connection.sink_port_index = sink_port_index
	
def make_voice_connection(instrument, source_index, source_port_index, sink_index, sink_port_index):
	connection = instrument.voice_connections.add()
	connection.source_index = source_index
	connection.source_port_index = source_port_index
	connection.sink_index = sink_index
	connection.sink_port_index = sink_port_index

def set_port_value(synth, plugin_index, port_index, the_value):
	plugin = synth.plugins[plugin_index]
	value = plugin.values.add()
	value.port_index = port_index
	value.value = the_value

def expose_port(synth, plugin_index, port_index):
	port = synth.exposed_ports.add()
	port.plugin_index = plugin_index
	port.port_index = port_index
	
TRIGGER = 0
GATE = 1
VELOCITY = 2
FREQUENCY = 3

