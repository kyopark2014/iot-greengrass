# Pub / Sub IPC

[Publish/subscribe local messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)와 [AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)를 참조하여 IPC로 PUBSUB을 통해 edge안에서 Local 메시지를 교환하는 방법에 대해 설명합니다. 



## Publish To IPC PUBSUB

IPC로 [MQTT 메시지를 PUBLISH 하는 예제](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/publisher/artifacts/com.example.Publisher/1.0.0/example_publisher.py)입니다. 5초에 한번씩 메시지를 다른 compnent들에게 전송합니다. 

```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import time
import datetime
import json
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    PublishToTopicRequest,
    PublishMessage,
    JsonMessage
)
from dummy_sensor import DummySensor

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()

sensor = DummySensor()

topic = "local/topic"

while True:
    message = {"timestamp": str(datetime.datetime.now()),
               "value": sensor.read_value()}
    message_json = json.dumps(message).encode('utf-8')

    request = PublishToTopicRequest()
    request.topic = topic
    publish_message = PublishMessage()
    publish_message.json_message = JsonMessage()
    publish_message.json_message.message = message
    request.publish_message = publish_message
    operation = ipc_client.new_publish_to_topic()
    operation.activate(request)
    future = operation.get_response()
    future.result(TIMEOUT)

    print(f"publish: {message_json}")
    time.sleep(5)
```

이때의 [Publisher에 대한 recipe](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-iotcore/publisher/recipes/com.iotcore.Publisher-1.0.0.json)는 아래와 같습니다.

```java
{
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "com.example.Publisher",
    "ComponentVersion": "1.0.0",
    "ComponentDescription": "A component that publishes messages.",
    "ComponentPublisher": "Amazon",
    "ComponentConfiguration": {
      "DefaultConfiguration": {
        "accessControl": {
          "aws.greengrass.ipc.pubsub": {
            "com.example.Publisher:pubsub:1": {
              "policyDescription": "Allows access to publish to all topics.",
              "operations": [
                "aws.greengrass#PublishToTopic"
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
          "Install": "pip3 install awsiotsdk numpy",
          "Run": "python3 -u {artifacts:path}/example_publisher.py"
        }
      }
    ]
}
```

## Subscribe To IPC PUBSUB

lifecycle이 끝나도 subscribe 할수 있도록 [IPC event stream](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)으로 정의합니다. 아래는 [local 메시지를 위하여 IPC를 Subscribe하는 예제](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/subsriber/artifacts/com.example.Subscriber/1.0.0/example_subscriber.py)입니다

```python
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import time
import json
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
        message_string = event.json_message.message

        # Handle message.
        with open('/tmp/Greengrass_Local_Subscriber.log', 'a') as f:
            print(message_string, file=f)

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass

topic = "local/topic"

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

operation.close()
```


이때의 [Subscriber에 대한 recipe](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/subsriber/recipes/com.example.Subscriber-1.0.0.json)는 아래와 같습니다.

```java
{
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "com.example.Subscriber",
    "ComponentVersion": "1.0.0",
    "ComponentDescription": "A component that subscribes to messages.",
    "ComponentPublisher": "Amazon",
    "ComponentConfiguration": {
      "DefaultConfiguration": {
        "accessControl": {
          "aws.greengrass.ipc.pubsub": {
            "com.example.Subscriber:pubsub:1": {
              "policyDescription": "Allows access to publish to all topics.",
              "operations": [
                "aws.greengrass#SubscribeToTopic"
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
          "Run": "python3 -u {artifacts:path}/example_subscriber.py"
        }
      }
    ]
}
```  


## 설치 및 시험


### 소스 다운로드 

소스를 다운로드 합니다.

```c
git clone https://github.com/kyopark2014/iot-greengrass
cd iot-greengrass/pubsub-ipc/publisher/
```

### Publisher 설치 

[publisher.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/publisher/publisher.sh)를 이용하여 Publisher를 설치합니다. 

```c
chmod a+x publisher.sh
./publisher.sh
```
```c
Aug 05, 2022 9:02:13 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 05, 2022 9:02:13 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: e40c64e4-6ab6-4eff-a0e6-989c4b0bbd3a
```

설치가 잘 되었는지를 로그로 확인합니다. 

```c
sudo tail /greengrass/v2/logs/com.example.Publisher.log
```

아래처럼 publish의 값을 통해 정상적으로 동작함을 확인 할 수 있습니다. 

```java
2022-08-06T07:15:20.612Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:20.611777", "value": 1022.23}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:25.618Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:25.617816", "value": 982.93}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:30.624Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:30.623747", "value": 999.9}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:35.630Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:35.629568", "value": 968.83}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:40.636Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:40.635418", "value": 999.61}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:45.642Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:45.641279", "value": 1016.0}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:50.651Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:50.647364", "value": 1018.59}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:15:55.657Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:15:55.656325", "value": 1024.87}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:16:00.663Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:16:00.662249", "value": 968.46}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-06T07:16:05.668Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-06 07:16:05.668095", "value": 1011.59}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
```

publisher 설치 상태는 아래와 같이 확인 할 수 있습니다.

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: com.example.Publisher
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.pubsub":{"com.example.Publisher:pubsub:1":{"operations":["aws.greengrass#PublishToTopic"],"policyDescription":"Allows access to publish to all topics.","resources":["*"]}}}}
```    

### Subscriber 설치 

[subscriber.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/subsriber/subscriber.sh)를 이용하여 Subscriber를 설치합니다. 

```java
cd iot-greengrass/pubsub-ipc/subscriber/
./subscriber.sh 
```

```java
Aug 05, 2022 9:33:08 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Aug 05, 2022 9:33:08 AM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: b4db7ef8-f98d-44d9-9fe2-9573b97c7ae1
```

로그로 설치 상태를 확인합니다. 

```java
sudo tail /greengrass/v2/logs/com.example.Subscriber.log
```

```java
2022-08-06T07:17:42.710Z [INFO] (Copier) com.example.Subscriber: stdout. Installing collected packages: awscrt, awsiotsdk. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-06T07:17:42.846Z [INFO] (Copier) com.example.Subscriber: stdout. Successfully installed awscrt-0.13.13 awsiotsdk-1.11.3. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-06T07:17:42.903Z [INFO] (pool-2-thread-38) com.example.Subscriber: shell-runner-start. {scriptName=services.com.example.Subscriber.lifecycle.Run, serviceName=com.example.Subscriber, currentState=STARTING, command=["python3 -u /greengrass/v2/packages/artifacts/com.example.Subscriber/1.0.0/exam..."]}
```

Subscriber가 받은 메시지는 아래와 같습니다. 

```java
tail -f /tmp/Greengrass_Local_Subscriber.log 
```
```java
{'timestamp': '2022-08-06 07:18:21.033849', 'value': 997.79}
{'timestamp': '2022-08-06 07:18:26.039932', 'value': 1007.6}
{'timestamp': '2022-08-06 07:18:31.046069', 'value': 1004.51}
{'timestamp': '2022-08-06 07:18:36.052169', 'value': 1039.45}
{'timestamp': '2022-08-06 07:18:41.055611', 'value': 991.49}
{'timestamp': '2022-08-06 07:18:46.061230', 'value': 986.72}
{'timestamp': '2022-08-06 07:18:51.067478', 'value': 997.51}
{'timestamp': '2022-08-06 07:18:56.073546', 'value': 970.32}
{'timestamp': '2022-08-06 07:19:01.079663', 'value': 1042.96}
{'timestamp': '2022-08-06 07:19:06.085763', 'value': 1011.12}
{'timestamp': '2022-08-06 07:19:11.091879', 'value': 993.91}
{'timestamp': '2022-08-06 07:19:16.093746', 'value': 1003.73}
{'timestamp': '2022-08-06 07:19:21.099855', 'value': 1010.17}
{'timestamp': '2022-08-06 07:19:26.105958', 'value': 994.62}
{'timestamp': '2022-08-06 07:19:31.112092', 'value': 994.19}
```

Subscriber의 상태는 아래와 같이 확인할 수 있습니다. 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```
```java
Component Name: com.example.Subscriber
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.pubsub":{"com.example.Subscriber:pubsub:1":{"operations":["aws.greengrass#SubscribeToTopic"],"policyDescription":"Allows access to publish to all topics.","resources":["*"]}}}}
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

[Publish/subscribe local messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)
