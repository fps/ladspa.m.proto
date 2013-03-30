from ladspam_pb2 import *

rack = Rack()

freeverb = rack.plugins.add()
freeverb.library = '/usr/lib/ladspa/cmt.so'
freeverb.label = 'freeverb3'

wet_value = freeverb.values.add()
wet_value.port_index = 8
wet_value.value = 0.3

room_size = freeverb.values.add()
room_size.port_index = 5
room_size.value = 0.8

sc4 = rack.plugins.add()
sc4.library = '/usr/lib/ladspa/sc4_1882.so'
sc4.label = 'sc4'

threshold = sc4.values.add()
threshold.port_index = 3
threshold.value = -10

ratio = sc4.values.add()
ratio.port_index = 4
ratio.value = 10

print(rack.SerializeToString())