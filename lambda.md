# Lambda Component


## Greengrass에서 Lambda component를 사용하는 경우

1) Lambda 함수에 있는 코드를 써야 하는 경우 

You have application code in Lambda functions that you want to deploy to core devices.

2) Greengrass V1으로 개발한 App을 V2에서 사용하고 싶은 경우

You have AWS IoT Greengrass V1 applications that you want to run on AWS IoT Greengrass V2 core devices.

## Dependencies

Lambda component를 사용하기 위해서는 아래 component들을 포함하여야 합니다. 

- [Lambda launcher component (aws.greengrass.LambdaLauncher)](https://docs.aws.amazon.com/greengrass/v2/developerguide/lambda-launcher-component.html): process들과 Environment configuration 관리합니다. Greengrass core device의 lambda function을 시작하고 종료하는데, containerization을 설정하고 process들을 동작시키는 일을 합니다. 

- [Lambda manager component (aws.greengrass.LambdaManager)](https://docs.aws.amazon.com/greengrass/v2/developerguide/lambda-manager-component.html): IPC(interprocess communication) and scaling을 관리합니다.

- [Lambda runtimes component (aws.greengrass.LambdaRuntimes)](https://docs.aws.amazon.com/greengrass/v2/developerguide/lambda-runtimes-component.html): Lambda runtime을 위한 artifacts를 제공합니다. 


## Lambda 함수 Lifecycle

- On-demand lifecycle: Invoke 될때마다 sandbox로 불리우는 다른 container를 생성하고 reuse 하지 않으며, task가 끝나면 종료합니다. 
- Long-lived (or pinned) lifecycle: Greengrass core software가 시작할때 single container로 시작하고 하나의 컨테이너가 모든 데이터를 처리합니다. 여러개의 invocation이 발생하면 queuing 하면서 순차적으로 처리합니다. Long-lived lambda 함수는 constantly running하는 경우에 유용하며, 디바이스가 데이터를 받기 시작할때 machine learning model을 로드하거나 시작할 수 있습니다. Long-lived인 Lambda 함수는 Greengrass core가 deployment나 reboot으로 재시작하더라도 계속 실행됩니다. [Understanding Container Reuse in AWS Lambda](https://aws.amazon.com/ko/blogs/compute/container-reuse-in-lambda/)에 좀더 상세한 정보가 있습니다. 


## Lambda 생성 

#### AWS Lambda mappings

- One Lambda to one component
- Refactor single AWS Lambda functions to multiple, dependent components

#### Import AWS Lambda functions to components

```c
aws greengrassv2 create-component-version --lambda-arn 
```

#### Map subscriptions to component via authorization templates

### Event source

Lambda의 event source로 local publish/subscribe 메시지들과 IoT Core MQTT 메시지들를 이용할 수 있습니다. 다른 Lambda 함수나 component들과 메시지를 주고 받기 위해서는 [legacy subscription router component](https://docs.aws.amazon.com/greengrass/v2/developerguide/legacy-subscription-router-component.html)를 설치하여야 합니다. 

이를 위해 Topic, Type을 설정하여야 하는데, Type에는 "Local publish/subscribe"와 "AWS IoT Core MQTT"가 있습니다. 

- Timeout: non-pinned lambda가 실행하는 시간, 기본 3초
- Status timeout: pinned일때 lambda manager component에 status를 업데이트하는 간격, 기본 60초
- Maximum queue size: 메시지 queue의 크기, 기본 1000개
- Maximum number of instances: non-pinned인 lambda 함수의 최대 숫자, 기본 100개
- Maximum idle time: non-pinned인 lambda 함수가 idle상태를 유지하는 시간, 기본 60초
- Encoding type: Lambda 함수가 지원하는 payload 형태, Json 또는 Binary (기본 Json)



## Hello World

[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)을 참조하여 Hello World component를 생성하여 봅니다. 

1) "example-lambda-python" 폴더를 생성합니다.

2) [hello-world-python](https://github.com/aws-samples/aws-greengrass-samples/blob/master/hello-world-python/greengrassHelloWorld.py)에서 "greengrassHelloWorld.py"를 다운로드 합니다. 

3) greengrasssdk를 다운로드합니다.

```c
git clone https://github.com/aws/aws-greengrass-core-sdk-python 
```

4) "example-lambda-python"에 greengrasssdk를 아래처럼 복사를 합니다. 

```c
cp -R aws-greengrass-core-sdk-python/greengrasssdk example-lambda-python/
```

5) lambda 함수에 업로드하기 위하여 압축을 합니다. 

```c
cd example-lambda-python
zip -r deploy.zip *
```

6) [[AWS Lambda] - [Functions]](https://ap-northeast-2.console.aws.amazon.com/lambda/home?region=ap-northeast-2#/functions)에서 [Create function]을 선택하고, [function name]에 "example-lambda-python"을 입력하고 [Runtime]으로 적절한 Python 라이브러리를 선택한 후에 [Create function]을 선택합니다. 

7) 상단 오른쪽의 [Upload from]에서 [.zip]을 선택한 후에 "deploy.zip"을 선택하여 업로드 합니다. 

8) 아래처럼 [Versions]에서 버전을 정의 합니다. 

![image](https://user-images.githubusercontent.com/52392004/182875433-879f8e0a-331b-4435-ae31-3d13061bed88.png)

9) Alias를 선택하여 아래처럼 [Name]으로 "v1"을 지정하고, [Version]은 1을 선택합니다. 

![image](https://user-images.githubusercontent.com/52392004/182875925-48bdff5a-9d72-4ec0-9847-a5e77ee0821a.png)

10) 

## Reference

[Run AWS Lambda functions](https://docs.aws.amazon.com/greengrass/v2/developerguide/run-lambda-functions.html)

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)


[Tutorial creating hello world greengrass Lambda (in Python)](https://www.youtube.com/watch?v=jvQsygmzov0)

[Tutorial for a Greengrass Lambda listening to an MQTT Topic](https://www.youtube.com/watch?v=z9ju6FJ3Xlo)

[rpi-greengrass](https://github.com/miman/rpi-greengrass/blob/master/hello-world/README.md)

[2020 Greengrass Demo | Person recognition & counting project using AWS Lambda](https://www.youtube.com/watch?v=bRWT_sbzGds)

[PersonCountingRaspberry on the Edge using AWS Greengrass](https://github.com/Rauchdimehdi/PersonCountingRaspberry)

[AWS Greengrass Core SDK for JavaScript](https://github.com/aws/aws-greengrass-core-sdk-js)

[What I  learned after a couple of weeks of using AWS IoT Greengrass](https://www.proud2becloud.com/what-i-learned-after-a-couple-of-weeks-of-using-aws-iot-greengrass/)

[AWS IoT Greengrass V2](https://catalog.us-east-1.prod.workshops.aws/workshops/5ecc2416-f956-4273-b729-d0d30556013f/en-US/chapter1-introduction)

[AWS IoT Core Lambda](https://velog.io/@markyang92/AWS-IoT-Core-Lambda)

[AWS Edge computing example with Lambda and IoT Greengrass (version 2)](https://medium.com/@rostyslav.myronenko/aws-edge-computing-example-with-lambda-and-iot-greengrass-version-2-aa68f2cc246)

[aws-iot-greengrass-project](https://github.com/rimironenko/aws-iot-greengrass-project)

## Troubleshooting

```java
2022-08-05T02:47:17.288Z [ERROR] (pool-2-thread-24) example-lambda-python: ipc_client.py:64,HTTP Error 400:Bad Request, b'No subscription exists for the source arn:aws:lambda:ap-northeast-2:677146750822:function:example-lambda-python:2 and subject hello/world. Deploy and configure aws.greengrass.LegacySubscriptionRouter component to support publishing from Lambdas.'. {serviceInstance=0, serviceName=example-lambda-python, currentState=RUNNING}
````

아래와 같이 사용한 코드가 IPC를 사용하지 않았기 때문에 발생한 문제점입니다. 

The legacy subscription router component is required only if your Lambda function uses the publish() function in the AWS IoT Greengrass Core SDK. If you update your Lambda function code to use the interprocess communication (IPC) interface in the AWS IoT Device SDK V2, you don't need to deploy the legacy subscription router component. For more information, see the following interprocess
