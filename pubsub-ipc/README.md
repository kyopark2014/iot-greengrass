# PUBSUB in IPC

## Publisher

1. 소스를 다운로드 합니다.

```c
git clone https://github.com/kyopark2014/iot-greengrass
cd iot-greengrass/pubsub-ipc/publisher/
```

2. [publisher.sh](https://github.com/kyopark2014/iot-greengrass/blob/main/pubsub-ipc/publisher/publisher.sh)를 이용하여 Publisher를 설치합니다. 

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
cd /greengrass/v2/
sudo chmod +rx logs
cat ./logs/com.example.Publisher.log
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

## Reference

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)
