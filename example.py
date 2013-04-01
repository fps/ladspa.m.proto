# Generates a very simple rack definition with just 
# a Freeverb and a SC4 plugin.

from ladspam_pb2 import *

instrument = Instrument()
instrument.number_of_voices = 5

synth = instrument.synth

# A freeverb

freeverb = synth.plugins.add()
freeverb.library = '/usr/lib/ladspa/cmt.so'
freeverb.label = 'freeverb3'

wet_value = freeverb.values.add()
wet_value.port_index = 7
wet_value.value = 0.9

room_size = freeverb.values.add()
room_size.port_index = 5
room_size.value = 0.95

# A stereo compressor

sc4 = synth.plugins.add()
sc4.library = '/usr/lib/ladspa/sc4_1882.so'
sc4.label = 'sc4'

threshold = sc4.values.add()
threshold.port_index = 3
threshold.value = -10

ratio = sc4.values.add()
ratio.port_index = 4
ratio.value = 10

# Inside connections

connection1 = synth.connections.add()
connection1.source_index = 0
connection1.source_port_index = 2
connection1.sink_index = 1
connection1.sink_port_index = 9

connection2 = synth.connections.add()
connection2.source_index = 0
connection2.source_port_index = 3
connection2.sink_index = 1
connection2.sink_port_index = 10

# Exposed Ports

input1 = synth.exposed_ports.add()
input1.plugin_index = 0
input1.port_index = 0

input2 = synth.exposed_ports.add()
input2.plugin_index = 0
input2.port_index = 1

output5 = synth.exposed_ports.add()
output5.plugin_index = 1
output5.port_index = 11

output6 = synth.exposed_ports.add()
output6.plugin_index = 1
output6.port_index = 12

f = open("/dev/stdout", "wb")
f.write(instrument.SerializeToString())
f.close()
