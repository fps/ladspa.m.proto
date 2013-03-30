# Generates a very simple instrument definition
# which is a kick drum with 2 voices

from ladspam_pb2 import *

kick = Instrument()


allocator = kick.voice_allocator
allocator.strategy = VoiceAllocator.ROUND_ROBIN


multisynth = kick.synth
multisynth.instances = 2

synth = multisynth.synth

exp = synth.plugins.add()
exp.label = 'dahdsr_fexp'

gen = synth.plugins.add()
gen.label = 'sawtooth_fa_oa'


rack = multisynth.output_rack

dist = rack.plugins.add()
dist.label = 'chebstortion'

trigger = multisynth.connections.add()
trigger.source_port_index = 128
trigger.sink_port_index = 1

gate = multisynth.connections.add()
gate.source_port_index = 129
gate.sink_port_index = 0

print(kick.SerializeToString())