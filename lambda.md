# Lambda Component 

Lambda 함수는 AWS의 대표적인 서버리스 서비스입니다. IoT Greengrass는 AWS Lambda를 Edge device에서 실행할 수 있는 환경을 제공함으로, S3와 같은 저장소나 DynamoDB/Timestream 같은 데이터베이스를 Greengrass에서 Lambda를 통해 편리하게 할용할 수 있습니다. Generic Component들도 AWS SDK를 이용해 같은 동작을 수행할 수 있지만, 기존 Lambda 함수를 그대로 사용할 수 있다는 장점이 있습니다. 

Greengrass의 lambda component는 AWS cloud에 deploy된 Lambda 함수를 Local에서 실행할 수 있도록 해주는데, 이때 event sources로는 topic을 통해서 local component가 전달하는 메시지나 IoT Core에서 전달되는 메시지를 event로 사용할 수 있습니다. event를 받으면 on-demend moded일때는 multi thread로 동작하고, long-lived 일때는 queue에 저장하였다가 순차적으로 실행하게 됩니다. 

Lambda component는 독립적으로 greengrass에서 정의되는것이 아니라, AWS Cloud에 있는 Lambda를 local에서 가져와서 이용하는것이므로, AWS Cloud에 있는 lambda의 Role과 같은 permission이 동일하게 적용됩니다. 또한, AWS Cloud의 Lambda 처럼 Environment variables을 지정하거나, memory size를 조정하거나, Disk를 Volume으로 등록하여 사용할 수 있습니다.  


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

## Event source

Lambda의 event source로 local publish/subscribe 메시지들과 IoT Core MQTT 메시지들를 이용할 수 있습니다. 다른 Lambda 함수나 component들과 메시지를 주고 받기 위해서는 [legacy subscription router component](https://docs.aws.amazon.com/greengrass/v2/developerguide/legacy-subscription-router-component.html)를 설치하여야 합니다. 

이를 위해 Topic, Type을 설정하여야 하는데, Type에는 "Local publish/subscribe"와 "AWS IoT Core MQTT"가 있습니다. 

- Timeout: non-pinned lambda가 실행하는 시간, 기본 3초
- Status timeout: pinned일때 lambda manager component에 status를 업데이트하는 간격, 기본 60초
- Maximum queue size: 메시지 queue의 크기, 기본 1000개
- Maximum number of instances: non-pinned인 lambda 함수의 최대 숫자, 기본 100개
- Maximum idle time: non-pinned인 lambda 함수가 idle상태를 유지하는 시간, 기본 60초
- Encoding type: Lambda 함수가 지원하는 payload 형태, Json 또는 Binary (기본 Json)


## Lambda 생성 

[Lambda Component 생성하기](https://github.com/kyopark2014/iot-greengrass/blob/main/lambda/README.md)를 참조하여, Python이나 Node.JS로 Lambda component를 생성 
할 수 있습니다.
 
## Lambda Component Recipe 예

```java
{
  "RecipeFormatVersion": "2020-01-25",
  "ComponentName": "example-lambda-python",
  "ComponentVersion": "8.0.0",
  "ComponentType": "aws.greengrass.lambda",
  "ComponentDescription": "v8",
  "ComponentPublisher": "AWS Lambda",
  "ComponentSource": "arn:aws:lambda:ap-northeast-2:123456789012:function:example-lambda-python:8",
  "ComponentConfiguration": {
    "DefaultConfiguration": {
      "lambdaExecutionParameters": {
        "EnvironmentVariables": {}
      },
      "containerParams": {
        "memorySize": 16384,
        "mountROSysfs": false,
        "volumes": {},
        "devices": {}
      },
      "containerMode": "GreengrassContainer",
      "timeoutInSeconds": 3,
      "maxInstancesCount": 100,
      "inputPayloadEncodingType": "json",
      "maxQueueSize": 1000,
      "pinned": true,
      "maxIdleTimeInSeconds": 60,
      "statusTimeoutInSeconds": 60,
      "pubsubTopics": {
        "0": {
          "topic": "core/topic",
          "type": "IOT_CORE"
        },
        "1": {
          "topic": "local/topic",
          "type": "PUB_SUB"
        },
        "2": {
          "topic": "#",
          "type": "IOT_CORE"
        }
      }
    }
  },
  "ComponentDependencies": {
    "aws.greengrass.LambdaLauncher": {
      "VersionRequirement": ">=2.0.0 <3.0.0",
      "DependencyType": "HARD"
    },
    "aws.greengrass.TokenExchangeService": {
      "VersionRequirement": ">=2.0.0 <3.0.0",
      "DependencyType": "HARD"
    },
    "aws.greengrass.LambdaRuntimes": {
      "VersionRequirement": ">=2.0.0 <3.0.0",
      "DependencyType": "SOFT"
    }
  },
  "Manifests": [
    {
      "Platform": {},
      "Lifecycle": {},
      "Artifacts": [
        {
          "Uri": "greengrass:lambda-artifact.zip",
          "Digest": "zxTD8KBV2eciihYJ2aSzJyDkia74Bp0gu66930kYKoI=",
          "Algorithm": "SHA-256",
          "Unarchive": "ZIP",
          "Permission": {
            "Read": "OWNER",
            "Execute": "NONE"
          }
        }
      ]
    }
  ],
  "Lifecycle": {
    "startup": {
      "requiresPrivilege": true,
      "script": "{aws.greengrass.LambdaLauncher:artifacts:path}/lambda-launcher start"
    },
    "setenv": {
      "AWS_GREENGRASS_LAMBDA_CONTAINER_MODE": "{configuration:/containerMode}",
      "AWS_GREENGRASS_LAMBDA_ARN": "arn:aws:lambda:ap-northeast-2:677146750822:function:example-lambda-python:8",
      "AWS_GREENGRASS_LAMBDA_FUNCTION_HANDLER": "lambda_function.lambda_handler",
      "AWS_GREENGRASS_LAMBDA_ARTIFACT_PATH": "{artifacts:decompressedPath}/lambda-artifact",
      "AWS_GREENGRASS_LAMBDA_CONTAINER_PARAMS": "{configuration:/containerParams}",
      "AWS_GREENGRASS_LAMBDA_STATUS_TIMEOUT_SECONDS": "{configuration:/statusTimeoutInSeconds}",
      "AWS_GREENGRASS_LAMBDA_ENCODING_TYPE": "{configuration:/inputPayloadEncodingType}",
      "AWS_GREENGRASS_LAMBDA_PARAMS": "{configuration:/lambdaExecutionParameters}",
      "AWS_GREENGRASS_LAMBDA_RUNTIME_PATH": "{aws.greengrass.LambdaRuntimes:artifacts:decompressedPath}/runtime/",
      "AWS_GREENGRASS_LAMBDA_EXEC_ARGS": "[\"python3.8\",\"-u\",\"/runtime/python/lambda_runtime.py\",\"--handler=lambda_function.lambda_handler\"]",
      "AWS_GREENGRASS_LAMBDA_RUNTIME": "python3.8"
    },
    "shutdown": {
      "requiresPrivilege": true,
      "script": "{aws.greengrass.LambdaLauncher:artifacts:path}/lambda-launcher stop; {aws.greengrass.LambdaLauncher:artifacts:path}/lambda-launcher clean"
    }
  }
}


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
