from ladspam_pb2 import *

# Run 
#
# python example_instrument.py > example_instrument.pb
#
# to generate an instrument definition file that can be loaded
# by e.g. the ladspa.m.lv2 plugin

# These are just some utility functions to make working with
# the generated python bindings for the protobuf definition easier
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
	

# We want to have a polyphony of three..
number_of_voices = 3


# Create an instrument
instrument = Instrument()

# Set the number of voices
instrument.number_of_voices = number_of_voices


# The instrument uses a synth definition, so let's get a reference to it
synth = instrument.synth


# Keep track of the current plugin count. This is useful for later
# hooking up the ports to the ports of the voices/
number_of_plugins = 0

for n in range(number_of_voices):
	# Every voice has one exponential envelope
	plugin = add_plugin(synth, 'dahdsr_fexp')
	
	# Set some envelope parameters (identical for each voice)
	set_port_value(plugin, 2, 0.0)
	set_port_value(plugin, 3, 0.0)
	set_port_value(plugin, 4, 0.0)
	set_port_value(plugin, 5, 0.8)
	set_port_value(plugin, 6, 0.3)
	set_port_value(plugin, 7, 0.2)
	
	
	number_of_plugins += 1

	# The oscillator for each voice
	plugin = add_plugin(synth, 'sawtooth_fa_oa')

	number_of_plugins += 1

	# A product to use the envelope output for the gain of the sawtooth oscillator
	add_plugin(synth, 'product_iaia_oa')

	number_of_plugins += 1

	# Hook up the outputs of the envelope and the oscillator to the inputs
	# of the product plugin
	make_connection(synth, number_of_plugins - 3, 8, number_of_plugins - 1, 0)
	make_connection(synth, number_of_plugins - 2, 1, number_of_plugins - 1, 1)
	
	# Hook up the trigger...
	make_voice_connection(instrument, n, 0, number_of_plugins - 3, 1)
	
	# ...gate...
	make_voice_connection(instrument, n, 1, number_of_plugins - 3, 0)
	
	# ...and frequency ports of the voice n to the envelope and oscillator ports
	make_voice_connection(instrument, n, 3, number_of_plugins - 2, 0)

	# Finally add a delay plugin to each voice
	plugin = add_plugin(synth, 'delay_5s')
	
	# But use a different delay time for each voice
	set_port_value(plugin, 0, (1 + n) * 0.250)
	
	# Setup the dry/wet port
	set_port_value(plugin, 1, 0.25)

	number_of_plugins += 1
	
	# And connect the output of the product to the delay input
	make_connection(synth, number_of_plugins - 2, 2, number_of_plugins - 1, 2)

# As a final step sum all the outputs of the different voices
add_plugin(synth, 'sum_iaia_oa')

number_of_plugins += 1

# Expose the single sum output twice, so we get two identical 
# outputs on two exposed ports
expose_port(synth, number_of_plugins - 1, 2)
expose_port(synth, number_of_plugins - 1, 2)

# And finally hookup the outputs of the delays to the input of the sum
for n in range(number_of_voices):
	make_connection(synth, 4 * n + 3, 3, number_of_plugins - 1, 0)
	pass

# And now write the instrument definition to stdout
f = open("/dev/stdout", "wb")
f.write(instrument.SerializeToString())
f.close()
