# Pub / Sub IPC

[Publish/subscribe local messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)와 [AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)를 참조하여 IPC로 PUBSUB을 통해 edge안에서 Local 메시지를 교환하는 방법에 대해 설명합니다. 

## 소스 다운로드 

소스를 다운로드 합니다.

```c
git clone https://github.com/kyopark2014/iot-greengrass
cd iot-greengrass/pubsub-ipc/publisher/
```

## Publisher 설치 

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

## Subscriber 설치 

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

## Reference

[Publish/subscribe local messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)
