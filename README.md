To create proto files:
python -m grpc_tools.protoc -I=protos --python_out=protos/ --grpc_python_out=protos/ protos/proto.proto
