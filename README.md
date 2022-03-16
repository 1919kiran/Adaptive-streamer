### To create proto files:
python -m grpc_tools.protoc --proto_path=. protos/proto.proto --python_out=. --grpc_python_out=.

### To create file:
base64 /dev/urandom | head -c 1000000 > dataset/data3.txt


### Steps to run the code
1. Download the code base using SSH or HTTPS link.
2. Install library using requirements.txt file.
3. update the IP address of client and server in config file.
4. run server using command: python server.py.
5. run client using command: python client.py.

> You can send your data by placing data in dataset folder and updating the data file name using config file.
