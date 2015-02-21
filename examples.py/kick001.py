from ladspam_pb2_util import *

number_of_voices = 2

instrument = Instrument()

instrument.number_of_voices = number_of_voices

synth = instrument.synth

voice_outs = []

for voice in range(number_of_voices):
	freq_env = add_plugin(synth, 'dahdsr_fexp')
	set_port_value(synth, freq_env, 5, 1)
	set_port_value(synth, freq_env, 6, 0)
	set_port_value(synth, freq_env, 7, 0.01)

	make_voice_connection(instrument, voice, GATE, freq_env, 0)
	make_voice_connection(instrument, voice, TRIGGER, freq_env, 1)
	
	freq_env_prod = add_plugin(synth, 'product_iaia_oa')
	set_port_value(synth, freq_env_prod, 0, 10500)
	make_connection(synth, freq_env, 8, freq_env_prod, 1)


	freq_env_sum = add_plugin(synth, 'sum_iaia_oa')
	
	make_connection(synth, freq_env_prod, 2, freq_env_sum, 0)
	make_voice_connection(instrument, voice, FREQUENCY, freq_env_sum, 1)


	osc = add_plugin(synth, 'ladspam-sine-osc')
	## set_port_value(synth, osc, 1, 1)
	
	make_connection(synth, freq_env_sum, 2, osc, 0)
	
	
	amp_env = add_plugin(synth, 'dahdsr_fexp')
	set_port_value(synth, amp_env, 5, 1)
	set_port_value(synth, amp_env, 6, 0.0)
	set_port_value(synth, amp_env, 7, 0.01)


	make_voice_connection(instrument, voice, GATE, amp_env, 0)
	make_voice_connection(instrument, voice, TRIGGER, amp_env, 1)
	
	amp_env_prod = add_plugin(synth, 'product_iaia_oa')

	make_connection(synth, amp_env, 8, amp_env_prod, 0)
	
	make_connection(synth, osc, 4, amp_env_prod, 1)
	
	voice_outs.append(amp_env_prod)
	
sum = add_plugin(synth, 'sum_iaia_oa')

for voice in range(number_of_voices):
	make_connection(synth, voice_outs[voice], 2, sum, 0)

expose_port(synth, sum, 2)
# expose_port(synth, sum, 2)

dump_instrument(instrument)
