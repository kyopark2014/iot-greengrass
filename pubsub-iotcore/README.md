# Pub / Sub IoT Core 

[Use the AWS IoT Device SDK to communicate with the Greengrass nucleus, other components, and AWS IoT Core](https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-subscribe-operations)를 참조하여 AWS IoT Core를 이용하여, PUBSUB으로 메시지를 교환하는 방법에 대해 설명합니다. 

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
Component Name: com.example.Subscriber
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.pubsub":{"com.example.Subscriber:pubsub:1":{"operations":["aws.greengrass#SubscribeToTopic"],"policyDescription":"Allows access to publish to all topics.","resources":["*"]}}}}
```    

## Reference

[Publish/subscribe AWS IoT Core MQTT messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)
