# Ubii message formats compiled for python

## How to use

- Import the required message type
- Instanciate an object of the type

```python
from proto.services.serviceRequest_pb2 import ServiceRequest

request = ServiceRequest()
request.topic = '/services/topic_list'
```
- For more information on the different message types and how to use them check out:
  - https://github.com/SandroWeber/ubii-msg-formats
  - https://protobuf.dev/getting-started/pythontutorial/