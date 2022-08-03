# Component 예제 

## Publish To IoT Core

IoT Core로 MQTT 메시지를 PUBLISH 하는 예제입니다. 여기서 QoS는 아래와 같이 정의 할 수 있습니다.

- AT_MOST_ONCE – QoS 0. The MQTT message is delivered at most once.
- AT_LEAST_ONCE – QoS 1. The MQTT message is delivered at least once.

```python
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()
                    
topic = "my/topic"
message = "Hello, World"
qos = QOS.AT_LEAST_ONCE

request = PublishToIoTCoreRequest()
request.topic_name = topic
request.payload = bytes(message, "utf-8")
request.qos = qos
operation = ipc_client.new_publish_to_iot_core()
operation.activate(request)
future_response = operation.get_response()
future_response.result(TIMEOUT)
```


## Subscribe To IoT Core

lifecycle이 끝나도 subscribe 할수 있도록 [IPC event stream](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)으로 정의합니다.

```java
import time
import traceback

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscriptionResponseMessage
)

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()
                    
class StreamHandler(client.SubscribeToTopicStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message_string = str(event.binary_message.message, "utf-8")
            # Handle message.
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass


topic = "my/topic"

request = SubscribeToTopicRequest()
request.topic = topic
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_topic(handler) 
operation.activate(request)
future_response = operation.get_response()
future_response.result(TIMEOUT)

# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)
    
# To stop subscribing, close the operation stream.
operation.close()
```
