# AWS IoT Greengrass


## Greengrass 특징 

v2.0부터 JVM으로 구동되므로 별도 컴파일 없이 구동 가능합니다. 

![image](https://user-images.githubusercontent.com/52392004/181129624-d2a73168-5a8d-4336-be98-1815664a6bff.png)

### Components

하나의 Component는 Receipe file과 Artifacts로 구성됩니다. 

Component의 dependency를 yaml 파일 안에 ComponentDependencies에 정의 할 수 있습니다. 

```java
---
RecipeFormatVersion: 2020-01-25
ComponentName: demo.example.hello_world
ComponentVersion: '1.0.0'
ComponentDescription: My first AWS IoT Greengrass component.
ComponentPublisher: Amazon
ComponentDependencies:
  aws.greengrass.TokenExchangeService:
    VersionRequirement: '>=0.0.0'
    DependencyType: HARD
ComponentConfiguration:
  DefaultConfiguration:
    Message: world
Manifests:
  - Platform:
      os: linux
    Lifecycle:
      Run: |
        while true; do
          python3 {artifacts:path}/hello_world.py \
            '{configuration:/Message}’
          sleep 5
        done
     Artifacts:
       - URI: s3://BUCKET/artifacts/demo.example.hello_world/…
```

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
