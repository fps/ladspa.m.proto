.PHONY: all

all: ladspam.proto
	protoc ladspam.proto --cpp_out . --python_out . --java_out .
