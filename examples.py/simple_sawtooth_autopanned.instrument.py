from ladspam_pb2 import *
import random

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
	connection = instrument.connections.add()
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
	
TRIGGER = 0
GATE = 1
VELOCITY = 2
FREQUENCY = 3

number_of_voices = 5

instrument = Instrument()
instrument.number_of_voices = number_of_voices

synth = instrument.synth

plugin_index = 0

for n in range(number_of_voices):
	plugin = add_plugin(synth, 'dahdsr_fexp')
	env = plugin_index	

	set_port_value(plugin, 2, 0.0)
	set_port_value(plugin, 3, 0.0)
	set_port_value(plugin, 4, 0.0)
	set_port_value(plugin, 5, 0.8)
	set_port_value(plugin, 6, 0.3)
	set_port_value(plugin, 7, 0.2)
	
	
	plugin_index += 1

	plugin = add_plugin(synth, 'sawtooth_fa_oa')
	osc = plugin_index

	plugin_index += 1

	add_plugin(synth, 'product_iaia_oa')
	prod = plugin_index

	make_connection(synth, env, 8, prod, 0)
	make_connection(synth, osc, 1, prod, 1)

	#print(plugin_index - 2, 8, plugin_index - 1, 1)
	 
	make_voice_connection(instrument, n, TRIGGER, env, 1)
	make_voice_connection(instrument, n, GATE, env, 0)
	make_voice_connection(instrument, n, FREQUENCY, osc, 0)

	plugin_index += 1

	plugin = add_plugin(synth, 'tap_autopan')
	pan = plugin_index

	set_port_value(plugin, 0, random.uniform(1, 5))
	set_port_value(plugin, 1, 50)

	make_connection(synth, prod, 2, pan, 3)
	make_connection(synth, prod, 2, pan, 4)

	plugin_index += 1
	

add_plugin(synth, 'sum_iaia_oa')
sum1 = plugin_index

expose_port(synth, sum1, 2)
plugin_index += 1

	
add_plugin(synth, 'sum_iaia_oa')
sum2 = plugin_index

expose_port(synth, sum2, 2)
plugin_index += 1
	
for n in range(number_of_voices):
	make_connection(synth, 4 * n + 3, 5, plugin_index - 1, 0)
	make_connection(synth, 4 * n + 3, 6, plugin_index - 2, 0)
	pass

f = open("/dev/stdout", "wb")
f.write(instrument.SerializeToString())
f.close()

