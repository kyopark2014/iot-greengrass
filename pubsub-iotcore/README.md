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

이때의 [Publisher에 대한 recipe](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/publisher/recipes/com.iotcore.Publisher-1.0.0.json)는 아래와 같습니다.

```java
{
      "RecipeFormatVersion": "2020-01-25",
      "ComponentName": "com.iotcore.Publisher",
      "ComponentVersion": "1.0.0",
      "ComponentDescription": "A component that publishes messages.",
      "ComponentPublisher": "Amazon",
      "ComponentConfiguration": {
        "DefaultConfiguration": {
          "accessControl": {
            "aws.greengrass.ipc.mqttproxy": {
              "com.iotcore.Publisher:mqttproxy:1": {
                "policyDescription": "Allows access to publish to all AWS IoT Core topics.",
                "operations": [
                  "aws.greengrass#PublishToIoTCore"
                ],
                "resources": [
                  "*"
                ]
              }
            }
          }
        }
      },
      "Manifests": [{
        "Platform": {
          "os": "linux"
        },
        "Lifecycle": {
          "Install": {
            "RequiresPrivilege": true,
            "Script": "sudo pip3 install awsiotsdk"
          },
          "Run": "python3 {artifacts:path}/iotcore_publisher.py"
        }
      }]
    }
```

## Subscribe To IoT Core

lifecycle이 끝나도 subscribe 할수 있도록 [IPC event stream](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)으로 정의합니다. 아래는 [IoT Core를 Subscribe하는 예제](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/subsriber/artifacts/com.iotcore.Subscriber/1.0.0/iotcore_subscriber.py)입니다

```python
import time
import traceback

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest
)

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()

class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            topic_name = event.message.topic_name

            print(f"publish({topic_name}): {message}")
            
            # Handle message.
            with open('/tmp/Greengrass_IoTCore_Subscriber.log', 'a') as f:
                print(message, file=f)
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass

topic = "core/topic"
qos = QOS.AT_MOST_ONCE

request = SubscribeToIoTCoreRequest()
request.topic_name = topic
request.qos = qos
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_iot_core(handler)
operation.activate(request)
future_response = operation.get_response() 
future_response.result(TIMEOUT)

# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)
                  
# To stop subscribing, close the operation stream.
operation.close()
```


이때의 [Subscriber에 대한 recipe](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/subsriber/recipes/com.iotcore.Subscriber-1.0.0.json)는 아래와 같습니다.

```java
{
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "com.iotcore.Subscriber",
    "ComponentVersion": "1.0.0",
    "ComponentDescription": "A component that subscribes to messages.",
    "ComponentPublisher": "Amazon",
    "ComponentConfiguration": {
      "DefaultConfiguration": {
        "accessControl": {
          "aws.greengrass.ipc.mqttproxy": {
            "com.iotcore.Subscriber:mqttproxy:1": {
              "policyDescription": "Allows access to subscribe to all AWS IoT Core topics.",
              "operations": [
                "aws.greengrass#SubscribeToIoTCore"
              ],
              "resources": [
                "*"
              ]
            }
          }
        }
      }
    },
    "Manifests": [
      {
        "Lifecycle": {
          "Install": "pip3 install awsiotsdk",
          "Run": "python3 -u {artifacts:path}/iotcore_subscriber.py"
        }
      }
    ]
}
```  


## 설치 및 시험

### 소스 다운로드 

소스를 아래와 같이 다운로드 합니다.

```c
git clone https://github.com/kyopark2014/iot-greengrass
cd iot-greengrass/pubsub-iotcore/publisher/
```

### Publisher 설치 

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



Publisher component의 상태는 아래와 같이 확인 할 수 있습니다.

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





### Subscriber 설치 

Component의 lifecycle이 끝나면 subscription이 remove되므로, Component는 event 메시지 streamdm으로 subscription을 하여야 합니다. 

[subscriber.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/subsriber/subscriber.sh)를 이용하여 Subscriber를 설치합니다. 

```java
cd iot-greengrass/pubsub-iotcore/subscriber/
./subscriber.sh 
```

```java
Aug 06, 2022 6:40:52 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 06, 2022 6:40:52 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: cc0a922b-a339-4af9-8534-d88756930c04
```

로그로 설치 상태를 확인합니다. 

```java
sudo tail logs/com.iotcore.Subscriber.log 
```
```java
2022-08-06T06:55:57.188Z [INFO] (Copier) com.iotcore.Subscriber: stdout. Installing collected packages: awscrt, awsiotsdk. {scriptName=services.com.iotcore.Subscriber.lifecycle.Install, serviceName=com.iotcore.Subscriber, currentState=NEW}
2022-08-06T06:55:57.361Z [INFO] (Copier) com.iotcore.Subscriber: stdout. Successfully installed awscrt-0.13.13 awsiotsdk-1.11.3. {scriptName=services.com.iotcore.Subscriber.lifecycle.Install, serviceName=com.iotcore.Subscriber, currentState=NEW}
2022-08-06T06:55:57.448Z [INFO] (pool-2-thread-26) com.iotcore.Subscriber: shell-runner-start. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=STARTING, command=["python3 -u /greengrass/v2/packages/artifacts/com.iotcore.Subscriber/1.0.0/iotc..."]}
2022-08-06T06:56:02.553Z [INFO] (Copier) com.iotcore.Subscriber: stdout. publish(core/topic): {"msg": "hello.world", "date": "2022-08-06 06:56:02.542674"}. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=RUNNING}
2022-08-06T06:56:07.559Z [INFO] (Copier) com.iotcore.Subscriber: stdout. publish(core/topic): {"msg": "hello.world", "date": "2022-08-06 06:56:07.548553"}. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=RUNNING}
2022-08-06T06:56:12.565Z [INFO] (Copier) com.iotcore.Subscriber: stdout. publish(core/topic): {"msg": "hello.world", "date": "2022-08-06 06:56:12.554378"}. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=RUNNING}
2022-08-06T06:56:17.571Z [INFO] (Copier) com.iotcore.Subscriber: stdout. publish(core/topic): {"msg": "hello.world", "date": "2022-08-06 06:56:17.560211"}. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=RUNNING}
2022-08-06T06:56:22.578Z [INFO] (Copier) com.iotcore.Subscriber: stdout. publish(core/topic): {"msg": "hello.world", "date": "2022-08-06 06:56:22.566034"}. {scriptName=services.com.iotcore.Subscriber.lifecycle.Run, serviceName=com.iotcore.Subscriber, currentState=RUNNING}
```

Subscriber가 받은 메시지는 아래와 같습니다. 

```java
tail -f /tmp/Greengrass_IoTCore_Subscriber.log
```

```java
{"msg": "hello.world", "date": "2022-08-06 06:58:42.712367"}
{"msg": "hello.world", "date": "2022-08-06 06:58:47.718273"}
{"msg": "hello.world", "date": "2022-08-06 06:58:52.724113"}
{"msg": "hello.world", "date": "2022-08-06 06:58:57.729954"}
{"msg": "hello.world", "date": "2022-08-06 06:59:02.735777"}
{"msg": "hello.world", "date": "2022-08-06 06:59:07.741631"}
{"msg": "hello.world", "date": "2022-08-06 06:59:12.745860"}
{"msg": "hello.world", "date": "2022-08-06 06:59:17.751731"}
{"msg": "hello.world", "date": "2022-08-06 06:59:22.756376"}
{"msg": "hello.world", "date": "2022-08-06 06:59:27.758600"}
```

Subscriber Component의 상태는 아래와 같이 확인할 수 있습니다. 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: com.iotcore.Subscriber
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.iotcore.Subscriber:mqttproxy:1":{"operations":["aws.greengrass#PublishToIoTCore","aws.greengrass#SubscribeToIoTCore"],"policyDescription":"Allows access to subscribe to all AWS IoT Core topics.","resources":["*"]}}}}
```    


### 유용한 명령어들

Component(예: com.iotcore.Subscriber)를 아래와 같이 삭제할 수 있습니다. 

```c
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.iotcore.Subscriber"
```

Greengrass 재시작이 필요한 경우에 아래와 같이 재시작 합니다.

```java
sudo systemctl restart greengrass.service
```

## Reference

[Publish/subscribe AWS IoT Core MQTT messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)

[Use the AWS IoT Device SDK to communicate with the Greengrass nucleus, other components, and AWS IoT Core](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)

[AWS IoT Greengrass Subscribe/Publish Component](https://velog.io/@markyang92/AWS-IoT-Greengrass-SubscribePublish-Component)
