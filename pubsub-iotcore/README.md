# Pub / Sub IoT Core 

[Publish/subscribe AWS IoT Core MQTT messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)를 참조하여 AWS IoT Core를 이용하여, PUBSUB으로 메시지를 교환하는 방법에 대해 설명합니다. 

## QOS 

QoS는 아래와 같이 정의 할 수 있습니다.

- AT_MOST_ONCE – QoS 0. The MQTT message is delivered at most once.
- AT_LEAST_ONCE – QoS 1. The MQTT message is delivered at least once.

## Publish To IoT Core

IoT Core로 [MQTT 메시지를 PUBLISH 하는 예제](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/publisher/artifacts/com.iotcore.Publisher/1.0.0/iotcore_publisher.py)입니다. 5초에 한번씩 메시지를 IoT Core로 전송합니다. 

```python
import time
import datetime
import json

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()
                    
topic = "core/topic"

while True:
    message = {
        "msg": "hello.world",
        "date": str(datetime.datetime.now()),
    }
    message_json = json.dumps(message).encode('utf-8')

    qos = QOS.AT_LEAST_ONCE
    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = message_json
    request.qos = qos

    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)
    future_response = operation.get_response()
    future_response.result(TIMEOUT)

    print(f"publish: {message_json}")
    time.sleep(5)
```


## Subscribe To IoT Core

lifecycle이 끝나도 subscribe 할수 있도록 [IPC event stream](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)으로 정의합니다.

```python
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


## hello_mqtt.py

```python
import json
import time
import os
import random

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    while True:
        telemetry_data = {
            "timestamp": int(round(time.time() * 1000)),
            "battery_level": random.randrange(98, 101),
            "location": {
                "longitude": round(random.uniform(101.0, 120.0),2),
                "latitude": round(random.uniform(30.0, 40.0),2),
            },
        }

        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name="ggv2/{}/telemetry".format(os.getenv("AWS_IOT_THING_NAME")),
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=1.0)
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(5)
```        




## 소스 다운로드 

소스를 다운로드 합니다.

```c
git clone https://github.com/kyopark2014/iot-greengrass
cd iot-greengrass/pubsub-iotcore/publisher/
```

## Publisher 설치 

[publisher.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/publisher/publisher.sh)를 이용하여 Publisher를 설치합니다. 

```c
chmod a+x publisher.sh
./publisher.sh
```
```c
Aug 05, 2022 1:58:16 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 05, 2022 1:58:16 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: d45850c6-5aa3-4f07-9717-31d199de1712
```

아래와 같이 Publisher의 로그를 확인하여 publish 동작을 확인합니다. 

```java
sudo tail /greengrass/v2/logs/com.iotcore.Publisher.log 
```

```java
2022-08-05T14:07:53.230Z [INFO] (Copier) com.iotcore.Publisher: stdout. publish: b'{"msg": "hello.world", "date": "2022-08-05 14:07:03.167195"}'. {scriptName=services.com.iotcore.Publisher.lifecycle.Run, serviceName=com.iotcore.Publisher, currentState=RUNNING}
2022-08-05T14:07:53.231Z [INFO] (Copier) com.iotcore.Publisher: stdout. publish: b'{"msg": "hello.world", "date": "2022-08-05 14:07:08.173429"}'. {scriptName=services.com.iotcore.Publisher.lifecycle.Run, serviceName=com.iotcore.Publisher, currentState=RUNNING}
2022-08-05T14:07:53.231Z [INFO] (Copier) com.iotcore.Publisher: stdout. publish: b'{"msg": "hello.world", "date": "2022-08-05 14:07:13.179648"}'. {scriptName=services.com.iotcore.Publisher.lifecycle.Run, serviceName=com.iotcore.Publisher, currentState=RUNNING}
2022-08-05T14:07:53.231Z [INFO] (Copier) com.iotcore.Publisher: stdout. publish: b'{"msg": "hello.world", "date": "2022-08-05 14:07:18.185660"}'. {scriptName=services.com.iotcore.Publisher.lifecycle.Run, serviceName=com.iotcore.Publisher, currentState=RUNNING}
2022-08-05T14:07:53.231Z [INFO] (Copier) com.iotcore.Publisher: stdout. publish: b'{"msg": "hello.world", "date": "2022-08-05 14:07:23.187923"}'. {scriptName=services.com.iotcore.Publisher.lifecycle.Run, serviceName=com.iotcore.Publisher, currentState=RUNNING}
```

동작을 확인하기 위하여 greengrass 재시작이 필요한 경우에 아래와 같이 재시작 합니다.

```java
sudo systemctl restart greengrass.service
```

publisher 설치 상태는 아래와 같이 확인 할 수 있습니다.

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: com.iotcore.Publisher
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.iotcore.Publisher:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish to all AWS IoT Core topics.","resources":["*"]}}}}
```    

[[AWS IoT] - [Test] - [MQTT test client]](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test)에서 아래와 같이 정상적으로 PUBLISH 된 데이터를 확인할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/183092845-a6884506-998b-4f70-8f0a-1ebd0d68d5cc.png)





## Subscriber 설치 

Component의 lifecycle이 끝나면 subscription이 remove되므로, Component는 event 메시지 streamdm으로 subscription을 하여야 합니다. 

[subscriber.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/subsriber/subscriber.sh)를 이용하여 Subscriber를 설치합니다. 

```java
cd iot-greengrass/pubsub-iotcore/subscriber/
./subscriber.sh 
```

```java
Aug 05, 2022 2:59:43 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 05, 2022 2:59:43 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: f017eaad-67b7-4ed2-91e7-e7fe1387f695
```

로그로 설치 상태를 확인합니다. 

```java
sudo tail logs/com.iotcore.Subscriber.log 
```

Subscriber가 받은 메시지는 아래와 같습니다. 

```java
tail -f /tmp/Greengrass_IoTSubscriber.log
```
```java
{'timestamp': '2022-08-05 09:35:17.812991', 'value': 990.55}
{'timestamp': '2022-08-05 09:35:18.815012', 'value': 984.51}
{'timestamp': '2022-08-05 09:35:19.817427', 'value': 994.84}
{'timestamp': '2022-08-05 09:35:20.819438', 'value': 1053.51}
{'timestamp': '2022-08-05 09:35:21.821950', 'value': 993.75}
{'timestamp': '2022-08-05 09:35:22.823961', 'value': 1026.83}
{'timestamp': '2022-08-05 09:35:23.825978', 'value': 962.5}
{'timestamp': '2022-08-05 09:35:24.828401', 'value': 984.66}
{'timestamp': '2022-08-05 09:35:25.830793', 'value': 987.71}
{'timestamp': '2022-08-05 09:35:26.832824', 'value': 1036.2}
{'timestamp': '2022-08-05 09:35:27.834464', 'value': 1045.2}
{'timestamp': '2022-08-05 09:35:28.835756', 'value': 967.77}
{'timestamp': '2022-08-05 09:35:29.837057', 'value': 1011.77}
{'timestamp': '2022-08-05 09:35:30.839504', 'value': 987.94}
```

Subscriber의 상태는 아래와 같이 확인할 수 있습니다. 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: com.iotcore.Subscriber
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.iotcore.Subscriber:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore","aws.greengrass#SubscribeToIoTCore"],"policyDescription":"Allows access to subscribe to all AWS IoT Core topics.","resources":["*"]}}}}
```    


## component 삭제 명령어

com.iotcore.Subscriber를 아래와 같이 삭제할 수 있습니다. 

```c
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.iotcore.Subscriber"
```



## Reference

[Publish/subscribe AWS IoT Core MQTT messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)

[Use the AWS IoT Device SDK to communicate with the Greengrass nucleus, other components, and AWS IoT Core](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)

[AWS IoT Greengrass Subscribe/Publish Component](https://velog.io/@markyang92/AWS-IoT-Greengrass-SubscribePublish-Component)
