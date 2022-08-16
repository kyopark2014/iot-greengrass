# Greengrass device에서 ML Inference

## ML source를 다운로드 


[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano ](https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/blob/main/README_kr.md)을 참조하여 ML이 포함된 component를 생성 및 배포하고자 합니다.

아래와 같이 git repository에서 소스를 다운로드 합니다. 

```c
$ git clone https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson
```



"greengrass-bucket" 버킷이 없는 경우에 아래 명령어로 생성합니다.

```c
$ aws s3 mb s3://greengrass-bucket
```

생성되었는지 아래와 같이 확인합니다. 

```c
$ aws s3 ls
2022-08-16 00:58:05 mybucket-677146750822
```


ggv2-deploy-cloud 디렉토리 아래에 있는 [config.json](https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/blob/main/ggv2-deploy-cloud/config.json)을 편집합니다. 여기서, Account에는 AWS 사용자 ID를 넣고, S3Bucket에 적당한 이름을 부여합니다. 여기서는 "greengrass-bucket"로 이름을 붙였습니다. 

```c
{
    "Project": {
        "Name": "MLInferenceFromScratch",
        "Account": "123456789012",
        "Region": "ap-northeast-2",
        "Profile": "ggv2-demo"
    },
    "Component": {
        "ComponentName": "com.example.ImgClassification",
        "ComponentVersion": "1.0.0",
        "SendMessage": "True",
        "Topic": "ml/example/imgclassification",
        "PredictionIntervalSecs": 3,
        "Timeout": 10
    },
    "Artifacts": {
        "S3Bucket": "greengrass-bucket",
        "S3Prefix": "ggv2/artifacts",
        "ZipArchiveName": "my-model"
    },
    "Parameters": {
        "UseGPU": 0,
        "ScoreThreshold": 0.25,
        "MaxNumClasses": 3,
        "ModelInputShape": "(224,224)"
    }
}
```


아래와 같이 "ggv2-deploy-cloud" 폴더의 "create_gg_component.sh"을 실행합니다. 

```c
cd aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/ggv2-deploy-cloud

sudo chmod +x create_gg_component.sh

./create_gg_component.sh
```

[create_gg_component.sh](https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/blob/main/ggv2-deploy-cloud/create_gg_component.sh)에 대한 상세 내용은 [aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson](https://github.com/kyopark2014/iot-greengrass/blob/main/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson.md)을 통해 이해합니다. 




상기와 같이 shell script를 실행하면 아래와 같은 결과를 얻을 수 있습니다. 

```c
$ aws greengrassv2 list-components
{
    "components": [
        {
            "componentName": "com.example.ImgClassification", 
            "latestVersion": {
                "publisher": "AWS", 
                "description": "Custom Image classification inference component using DLR.", 
                "componentVersion": "1.0.0", 
                "platforms": [
                    {
                        "attributes": {
                            "os": "linux"
                        }
                    }
                ], 
                "creationTimestamp": 1655244071.301, 
                "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.ImgClassification:versions:1.0.0"
            }, 
            "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.ImgClassification"
        },
    ]
}
```

component 등록 현황은 아래와 같이 확인 할 수 있습니다. 

```java
$ aws greengrassv2 list-components
{
    "components": [
        {
            "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.ImgClassification",
            "componentName": "com.example.ImgClassification",
            "latestVersion": {
                "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.ImgClassification:versions:1.0.0",
                "componentVersion": "1.0.0",
                "creationTimestamp": 1660620526.199,
                "description": "Custom Image classification inference component using DLR.",
                "publisher": "AWS",
                "platforms": [
                    {
                        "attributes": {
                            "os": "linux"
                        }
                    }
                ]
            }
        },
    ]
}
```

로그는 아래와 같이 확인합니다. 

```java
$ sudo /greengrass/v2/logs $ cat com.example.ImgClassification.log 

2022-08-16T03:39:23.730Z [INFO] (Copier) com.example.ImgClassification: stdout. {scriptName=services.com.example.ImgClassification.lifecycle.Run.script, serviceName=com.example.ImgClassification, currentState=RUNNING}
2022-08-16T03:39:23.730Z [INFO] (Copier) com.example.ImgClassification: stdout. image path = /greengrass/v2/packages/artifacts-unarchived/com.example.ImgClassification/1.0.0/my-model/sample_images/red_abnormal.jpg. {scriptName=services.com.example.ImgClassification.lifecycle.Run.script, serviceName=com.example.ImgClassification, currentState=RUNNING}
2022-08-16T03:39:23.765Z [INFO] (Copier) com.example.ImgClassification: stdout. {'message': '{"class_id":"5","class":"red_abnormal","score":"0.933888"}', 'timestamp': '2022-08-16T03:39:23'}. {scriptName=services.com.example.ImgClassification.lifecycle.Run.script, serviceName=com.example.ImgClassification, currentState=RUNNING}
2022-08-16T03:39:23.766Z [INFO] (Copier) com.example.ImgClassification: stdout. Publishing results to the IoT core.... {scriptName=services.com.example.ImgClassification.lifecycle.Run.script, serviceName=com.example.ImgClassification, currentState=RUNNING}
```

Deploy후에 아래와 같이 확인할 수 있습니다. 

```java
$ sudo /greengrass/v2/bin/greengrass-cli component list

Component Name: com.example.ImgClassification
    Version: 1.0.0
    State: RUNNING
    Configuration: {"accessControl":{"aws.greengrass.ipc.mqttproxy":{"com.example.Pub:publisher:1":{"operations":["aws.greengrass#PublishToIoTCore"],"policyDescription":"Allows access to publish to ml/example/imgclassification topic.","resources":["ml/example/imgclassification"]}}}}
```

이것을 [IoT Core의 Test Client](https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test)에서 "ml/example/imgclassification"로 subscribe시에 아래와 같이 결과를 확인 할 수 있습니다. 

<img width="1095" alt="image" src="https://user-images.githubusercontent.com/52392004/184795584-b2227fe3-8659-4348-a3b1-fc1a686257d2.png">

