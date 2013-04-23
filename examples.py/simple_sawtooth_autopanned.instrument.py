from ladspam_pb2 import *
import random

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
	connection = instrument.connections.add()
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

number_of_voices = 5

instrument = Instrument()
instrument.number_of_voices = number_of_voices

synth = instrument.synth

voice_outs = []

for n in range(number_of_voices):
	env = add_plugin(synth, 'dahdsr_fexp')

	set_port_value(synth, env, 2, 0.0)
	set_port_value(synth, env, 3, 0.0)
	set_port_value(synth, env, 4, 0.0)
	set_port_value(synth, env, 5, 0.8)
	set_port_value(synth, env, 6, 0.3)
	set_port_value(synth, env, 7, 0.2)
	
	osc = add_plugin(synth, 'sawtooth_fa_oa')

	env_prod = add_plugin(synth, 'product_iaia_oa')

	make_connection(synth, env, 8, env_prod, 0)
	make_connection(synth, osc, 1, env_prod, 1)

	make_voice_connection(instrument, n, TRIGGER, env, 1)
	make_voice_connection(instrument, n, GATE, env, 0)
	make_voice_connection(instrument, n, FREQUENCY, osc, 0)

	vel_prod = add_plugin(synth, 'product_iaia_oa')
	make_voice_connection(instrument, n, VELOCITY, vel_prod, 0)
	make_connection(synth, env_prod, 2, vel_prod, 1)

	pan = add_plugin(synth, 'tap_autopan')

	set_port_value(synth, pan, 0, random.uniform(0.1, 0.2))
	set_port_value(synth, pan, 1, 50)
	set_port_value(synth, pan, 2, 0)

	make_connection(synth, vel_prod, 2, pan, 3)
	make_connection(synth, vel_prod, 2, pan, 4)
	
	voice_outs.append(pan)


sum1 = add_plugin(synth, 'sum_iaia_oa')
sum2 = add_plugin(synth, 'sum_iaia_oa')

for n in range(number_of_voices):
	make_connection(synth, voice_outs[n], 5, sum1, 0)
	make_connection(synth, voice_outs[n], 6, sum2, 0)
	pass

final_pan = add_plugin(synth, 'tap_autopan')
set_port_value(synth, final_pan, 0, 0.1)
set_port_value(synth, final_pan, 1, 50)

make_connection(synth, sum1, 2, final_pan, 3)
make_connection(synth, sum2, 2, final_pan, 4)

expose_port(synth, final_pan, 5)
expose_port(synth, final_pan, 6)
	
f = open("/dev/stdout", "wb")
f.write(instrument.SerializeToString())
f.close()

