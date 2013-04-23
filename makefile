.PHONY: all install examples 

PREFIX ?= /usr/local

all: libladspam.pb.so
	python2 setup.py build

libladspam.pb.so: generated
	g++ -shared -fPIC -o libladspam.pb.so ladspam.pb.cc `pkg-config protobuf --cflags --libs`

generated: ladspam.proto
	protoc ladspam.proto --cpp_out . --python_out . 
	touch generated

install: all
	install -d $(PREFIX)/lib
	install libladspam.pb.so $(PREFIX)/lib
	install -d $(PREFIX)/include
	install ladspam.pb.h $(PREFIX)/include
	python2 setup.py install


examples:  
	bash generate_examples.sh

