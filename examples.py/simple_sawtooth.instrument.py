from ladspam_pb2 import *

def add_plugin(synth, label):
	plugin = synth.plugins.add()
	plugin.label = label
	return plugin

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

def set_port_value(plugin, port_index, the_value):
	value = plugin.values.add()
	value.port_index = port_index
	value.value = the_value

def expose_port(synth, plugin_index, port_index):
	port = synth.exposed_ports.add()
	port.plugin_index = plugin_index
	port.port_index = port_index
	

number_of_voices = 3

instrument = Instrument()
instrument.number_of_voices = number_of_voices

synth = instrument.synth

number_of_plugins = 0

for n in range(number_of_voices):
	plugin = add_plugin(synth, 'dahdsr_fexp')
	set_port_value(plugin, 2, 0.0)
	set_port_value(plugin, 3, 0.0)
	set_port_value(plugin, 4, 0.0)
	set_port_value(plugin, 5, 0.8)
	set_port_value(plugin, 6, 0.3)
	set_port_value(plugin, 7, 0.2)
	
	
	number_of_plugins += 1

	plugin = add_plugin(synth, 'sawtooth_fa_oa')
	# set_port_value(plugin, 0, 4 * 880)

	number_of_plugins += 1

	add_plugin(synth, 'product_iaia_oa')

	number_of_plugins += 1

	make_connection(synth, number_of_plugins - 3, 8, number_of_plugins - 1, 0)
	make_connection(synth, number_of_plugins - 2, 1, number_of_plugins - 1, 1)
	
	#print(number_of_plugins - 2, 8, number_of_plugins - 1, 1)
	 
	make_voice_connection(instrument, n, 0, number_of_plugins - 3, 1)
	make_voice_connection(instrument, n, 1, number_of_plugins - 3, 0)
	make_voice_connection(instrument, n, 3, number_of_plugins - 2, 0)

	plugin = add_plugin(synth, 'delay_5s')
	set_port_value(plugin, 0, (1 + n) * 0.250)
	set_port_value(plugin, 1, 0.25)

	number_of_plugins += 1
	
	make_connection(synth, number_of_plugins - 2, 2, number_of_plugins - 1, 2)

add_plugin(synth, 'sum_iaia_oa')

number_of_plugins += 1
	
expose_port(synth, number_of_plugins - 1, 2)
expose_port(synth, number_of_plugins - 1, 2)

for n in range(number_of_voices):
	make_connection(synth, 4 * n + 3, 3, number_of_plugins - 1, 0)
	pass

f = open("/dev/stdout", "wb")
f.write(instrument.SerializeToString())
f.close()