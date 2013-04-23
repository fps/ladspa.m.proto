# ladspa.m.proto

Protobuf definitions for defining synths and instruments made up of LADSPA synths.

# What?

The ladspam.proto file defines a message/file format for synth/instrument definitions. The generated libraries (C++ and python) can be used to read/write these definition files. See the examples 

https://github.com/fps/ladspa.m.proto/blob/master/examples.py

for a python script that generates and instrument definition file for a simple polyphonic instrument with sawtooth oscillators and exponential envelopes.

You can then load this instrument definition into a "host". There exist two implementations:

https://github.com/fps/ladspa.m.jack

and

https://github.com/fps/ladspa.m.lv2

The former provides standalone jack clients to load synth or instrument definitions. The latter provides an LV2 plugin that can load instrument definitions.

# Requirements

* protobuf, python

# Building

type

<pre>
make
</pre>

You can generate the example definition files by typing:

<pre>
make examples
</pre>

which will run the python scripts in examples.py to generate the corresponding definition files in examples.pb.

# Installation

type

<pre>
make install
</pre>

preferrably as superuser

# License 

LGPL v2.0 or later (see the file LICENSE)

# Author 

Florian Paul Schmidt (mista.tapas@gmx.net)
