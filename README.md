# AWS IoT Greengrass


## Greengrass 특징 

Greengrass v2.0부터는 Java기반으로 Core가 변경되어서, 별도 컴파일 없이 구동 가능합니다. [Greengrass](https://github.com/kyopark2014/iot-greengrass/blob/main/basic.md)는 Greengrass.jar와 [components](https://github.com/kyopark2014/iot-greengrass/blob/main/components.md)로 구성되는데, component에는 AWS가 제공하는 necleus, streammanger 등이 있으며, 사용자가 compoenent를 recipt를 이용해 직접 정의 할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/181129624-d2a73168-5a8d-4336-be98-1815664a6bff.png)

### Components

[Greengrass component](https://github.com/kyopark2014/iot-greengrass/blob/main/components.md)는 Greengrass core device를 구동하는 소프트웨어입니다. 이를 이용하여 local에서 core device를 개발하고 시험할 수 있습니다. Greengrass에서는 기본기능(basic feature)과 공통 라이브러리(common liabrary)를 비롯한 local 개발 툴을 components로 제공합니다. 

[Docker 이미지를 이용](https://github.com/kyopark2014/iot-greengrass/blob/main/docker-component.md)하여 Component를 생성할 수 있습니다. 생성된 Component는 cloud를 이용하여 다른 [device에 배포](https://github.com/kyopark2014/iot-greengrass/blob/main/deployment.md) 할 수 있습니다. 

또한, [Lambda를 Component로 등록](https://github.com/kyopark2014/iot-greengrass/blob/main/lambda.md)하여 사용할 수 있습니다. 

### Component간 통신방법

Greengrass의 Components들은 [IPC 통신](https://github.com/kyopark2014/iot-greengrass/blob/main/IPC.md)을 통해 Necleus와 연결되고, Components 사이는 [MQTT](https://github.com/kyopark2014/IoT-Core-Contents/blob/main/mqtt.md) PUBSUB으로 메시지를 교환할 수 있습니다. 

### Component examples

[Component 예제](https://github.com/kyopark2014/iot-greengrass/blob/main/component-examples.md)에서는 component를 위한 예제를 보여줍니다. 


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


## Reference

[Troubleshooting identity and access issues for AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/v1/developerguide/security_iam_troubleshoot.html)

[Troubleshooting AWS IoT Greengrass V2](https://docs.aws.amazon.com/greengrass/v2/developerguide/troubleshooting.html)

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
