# Pub / Sub IPC

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)를 참조하여 IPC로 PUBSUB을 통해 edge안에서 Local 메시지를 교환하는 방법에 대해 설명합니다. 

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
2022-08-05T09:13:18.495Z [INFO] (pool-2-thread-18) com.example.Publisher: shell-runner-start. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW, command=["pip3 install awsiotsdk numpy"]}
2022-08-05T09:13:20.192Z [INFO] (Copier) com.example.Publisher: stdout. Collecting awsiotsdk. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:20.264Z [INFO] (Copier) com.example.Publisher: stdout. Using cached https://files.pythonhosted.org/packages/0a/f0/3bb81c3c53bb5fb30a694ce72e64c4c04d327015d263a2f5309c43eca510/awsiotsdk-1.11.3-py3-none-any.whl. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:20.270Z [INFO] (Copier) com.example.Publisher: stdout. Collecting numpy. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:20.955Z [INFO] (Copier) com.example.Publisher: stdout. Using cached https://files.pythonhosted.org/packages/45/b2/6c7545bb7a38754d63048c7696804a0d947328125d81bf12beaa692c3ae3/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:21.331Z [INFO] (Copier) com.example.Publisher: stdout. Collecting awscrt==0.13.13 (from awsiotsdk). {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:21.968Z [INFO] (Copier) com.example.Publisher: stdout. Using cached https://files.pythonhosted.org/packages/3a/56/f830ec0dda86a1c4736ea8554d8a59c3c9102aaa565bcfcdbc8b5be65c53/awscrt-0.13.13-cp36-cp36m-manylinux_2_5_x86_64.manylinux1_x86_64.whl. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:22.125Z [INFO] (Copier) com.example.Publisher: stdout. Installing collected packages: awscrt, awsiotsdk, numpy. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:23.753Z [INFO] (Copier) com.example.Publisher: stdout. Successfully installed awscrt-0.13.13 awsiotsdk-1.11.3 numpy-1.19.5. {scriptName=services.com.example.Publisher.lifecycle.Install, serviceName=com.example.Publisher, currentState=NEW}
2022-08-05T09:13:23.832Z [INFO] (pool-2-thread-18) com.example.Publisher: shell-runner-start. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=STARTING, command=["python3 -u /greengrass/v2/packages/artifacts/com.example.Publisher/1.0.0/examp..."]}
2022-08-05T09:13:23.947Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-05 09:13:23.929729", "value": 997.67}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-05T09:13:24.950Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-05 09:13:24.948927", "value": 958.19}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-05T09:13:25.952Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-05 09:13:25.951170", "value": 1011.79}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-05T09:13:26.954Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-05 09:13:26.953454", "value": 985.02}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
2022-08-05T09:13:27.956Z [INFO] (Copier) com.example.Publisher: stdout. publish: b'{"timestamp": "2022-08-05 09:13:27.955693", "value": 1010.91}'. {scriptName=services.com.example.Publisher.lifecycle.Run, serviceName=com.example.Publisher, currentState=RUNNING}
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
cat com.example.Subscriber.log 
```

```java
2022-08-05T09:33:20.896Z [INFO] (pool-2-thread-34) com.example.Subscriber: shell-runner-start. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW, command=["pip3 install awsiotsdk"]}
2022-08-05T09:33:21.828Z [INFO] (Copier) com.example.Subscriber: stdout. Collecting awsiotsdk. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:22.104Z [INFO] (Copier) com.example.Subscriber: stdout. Using cached https://files.pythonhosted.org/packages/0a/f0/3bb81c3c53bb5fb30a694ce72e64c4c04d327015d263a2f5309c43eca510/awsiotsdk-1.11.3-py3-none-any.whl. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:22.111Z [INFO] (Copier) com.example.Subscriber: stdout. Collecting awscrt==0.13.13 (from awsiotsdk). {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:22.958Z [INFO] (Copier) com.example.Subscriber: stdout. Using cached https://files.pythonhosted.org/packages/3a/56/f830ec0dda86a1c4736ea8554d8a59c3c9102aaa565bcfcdbc8b5be65c53/awscrt-0.13.13-cp36-cp36m-manylinux_2_5_x86_64.manylinux1_x86_64.whl. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:23.122Z [INFO] (Copier) com.example.Subscriber: stdout. Installing collected packages: awscrt, awsiotsdk. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:23.264Z [INFO] (Copier) com.example.Subscriber: stdout. Successfully installed awscrt-0.13.13 awsiotsdk-1.11.3. {scriptName=services.com.example.Subscriber.lifecycle.Install, serviceName=com.example.Subscriber, currentState=NEW}
2022-08-05T09:33:23.334Z [INFO] (pool-2-thread-34) com.example.Subscriber: shell-runner-start. {scriptName=services.com.example.Subscriber.lifecycle.Run, serviceName=com.example.Subscriber, currentState=STARTING, command=["python3 -u /greengrass/v2/packages/artifacts/com.example.Subscriber/1.0.0/exam..."]}
```

Subscriber가 받은 메시지는 아래와 같습니다. 

```java
tail -f /tmp/Greengrass_Subscriber.log
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

[Publish/subscribe local messages](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)
