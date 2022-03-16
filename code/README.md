### To create proto files:
python -m grpc_tools.protoc --proto_path=. protos/proto.proto --python_out=. --grpc_python_out=.

### To create file:
base64 /dev/urandom | head -c 1000000 > dataset/data3.txt
