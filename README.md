# IoT Greengrass

IoT Greengrass는 IoT를 위한 오픈소스 edge runtime으로서, Edge 디바이스의 Component를 build하고 deploy하며, manage하는 cloud 서비스입니다. 이를 이용하여 수백만개의 디바이스를 집, 공장, 자동차와 비지니스에서 활용할 수 있습니다. [IoT Greengrass Basic](https://github.com/kyopark2014/iot-greengrass/blob/main/basic.md)에서 Greengress에 대해 설명합니다.

## Greengrass 특징 

Greengrass V2는 Java기반 Core를 사용하므로, 별도 컴파일 없이 구동 가능합니다. Greengrass는 Greengrass.jar와 [components](https://github.com/kyopark2014/iot-greengrass/blob/main/components.md)로 구성되는데, component에는 AWS가 제공하는 necleus, streammanger 등이 있으며, 사용자가 compoenent를 recipe를 이용해 직접 정의 할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/181129624-d2a73168-5a8d-4336-be98-1815664a6bff.png)

### Components

[Greengrass component](https://github.com/kyopark2014/iot-greengrass/blob/main/components.md)는 Greengrass core device를 구동하는 소프트웨어입니다. Greengrass에서는 기본 기능(basic feature)과 공통 라이브러리(common library)를 비롯한 local 개발 툴을 components로 제공하며, Greengrass CLI를 이용하여 Local에서 core device를 개발하고 시험할 수 있습니다. 또는 Component는 cloud를 이용하여 다수의 [device에 배포](https://github.com/kyopark2014/iot-greengrass/blob/main/deployment.md) 할 수 있습니다. 

### Component간 통신방법

Greengrass의 Components들은 [IPC 통신](https://github.com/kyopark2014/iot-greengrass/blob/main/IPC.md)을 통해 Necleus와 연결되고, Components 사이는 [MQTT](https://github.com/kyopark2014/IoT-Core-Contents/blob/main/mqtt.md) PUBSUB으로 메시지를 교환할 수 있습니다. Component들은 아래의 1,2,3과 같이 Greengrass 내부의 component들간에 [local message를 교환](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)할 수 있고, 1,2,4와 같이 IoT Core를 통해 메시지를 교환할 수 있습니다. 

- [Pub/Sub IPC](https://github.com/kyopark2014/iot-greengrass/tree/main/pubsub-ipc)에서는 edge에 설치된 component들 끼리, PUBSUB을 이용하여 IPC로 통신하는 방법을 보여줍니다.  

- [Pub/Sub IoT Core](https://github.com/kyopark2014/iot-greengrass/tree/main/pubsub-iotcore)에서는 edge에 설치된 component가 IoT Core와 PUBSUB을 이용하여 MQTT로 통신하는 방법을 보여줍니다. 


![image](https://user-images.githubusercontent.com/52392004/181382025-d2a786dd-b2f1-46a7-9cc5-065ae749c54d.png)

그림의 [local PubSub](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-publish-subscribe.html)의 IPC service identifier은 "aws.greengrass.ipc.pubsub"이고, [IoTMQTTClient](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)는 "aws.greengrass.ipc.mqttproxy" 입니다. 


### Lambda Component

[Lambda를 Component로 등록](https://github.com/kyopark2014/iot-greengrass/blob/main/lambda.md)하여 사용할 수 있습니다. 


### Docker Component

[Docker 이미지를 이용](https://github.com/kyopark2014/iot-greengrass/blob/main/docker-component.md)하여 Component를 생성할 수 있습니다. 



### Credentials Provider Workflow

[Credentials Provider Workflow](https://github.com/kyopark2014/iot-greengrass/blob/main/credentials-provider-workflow.md)

## Greengrass 계정 생성

Greengrass 사용시 보안을 위하여 기능이 제한된 계정을 사용하여야 합니다. 이를 위해 [Greengrass를 위한 계정 등록](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-user-registration.md)에 따라 계정을 생성합니다. 

## Greengrass Commands와 Memo

유용한 [Greengrass 명령어와 중요한 메모들](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-commands.md)를 정리하였습니다.

### v2.0과 v1.0의 차이점 

상세한 차이점은 [Greengrass Version](https://github.com/kyopark2014/iot-greengrass/blob/main/version-difference.md)을 참고 바랍니다. 

- Core software
- Components
- Inter-process communication (IPC)
- Docker containers
- Nucleus and component security
- Operating system integration and interaction

## Greengress Workshop

1) [Workshop Greengrass](https://github.com/kyopark2014/iot-greengrass/blob/main/workshop-greengrass-beginner.md)을 따라서, Cloud9에 Greengrass V2를 설치하고, Local에서 배포를 수행합니다. 

2) [Amazon S3를 이용하여 Greengrass Component를 배포하기](https://github.com/kyopark2014/iot-greengrass/blob/main/workshop-s3-deployment.md)에 따라, Amazon S3를 통해 배포환경을 구성 합니다.

3) [Greengrass device에서 ML Inference](https://github.com/kyopark2014/iot-greengrass/blob/main/workshop-ml.md)에 따라, ML source를 다운로드하여 Greengrass component로 배포할 수 있습니다. 


## EC2(Linux)에서 Greengrass 설치 및 배포

1) EC2에 Greengrass 설치

[EC2에 Greengrass 설치하기](https://github.com/kyopark2014/iot-greengrass/blob/main/ec2-greengrass.md)에 따라서 Greengrass를 설치합니다. 


2) [Greengrass CLI 설치](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-cli.md)에 따라 Greengrass CLI를 설치합니다.

3) Greengrass components 생성

[Greengreen Component](https://github.com/kyopark2014/iot-greengrass/blob/main/greengrass-component.md)을 따라서, receipe와 artifact을 생성합니다.

4) Device에서 ML Inference

[디바이스에서의 ML Inference](https://github.com/kyopark2014/iot-greengrass/blob/main/ML-inference.md)을 이용하여 ML을 실행할 수 있습니다.

## Raspberry Pi에 Greengrass 설치 및 배포

[Raspberry Pi](https://github.com/kyopark2014/iot-greengrass/blob/main/raspberry-pi.md)에 Greengrass를 설치합니다. 

## Reference

[AWS IoT Greengrass](https://github.com/aws-greengrass/)

[Troubleshooting identity and access issues for AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/v1/developerguide/security_iam_troubleshoot.html)

[Troubleshooting AWS IoT Greengrass V2](https://docs.aws.amazon.com/greengrass/v2/developerguide/troubleshooting.html)

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
