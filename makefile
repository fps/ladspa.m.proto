.PHONY: all install

PREFIX ?= /usr/local

all: libladspam.pb.so

libladspam.pb.so: generated
	g++ -shared -fPIC -o libladspam.pb.so ladspam.pb.cc `pkg-config protobuf --cflags --libs`

generated: ladspam.proto
	protoc ladspam.proto --cpp_out . --python_out . 
	touch generated

install: all
	install -d $(PREFIX)/lib
	install libladspam.pb.so $(PREFIX)/lib

