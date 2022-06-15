# Greengrass device에서 ML Inference

## ML source를 다운로드 


[End-to-end AIoT w/ SageMaker and Greengrass 2.0 on NVIDIA Jetson Nano ](https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/blob/main/README_kr.md)을 참조하여 ML이 포함된 component를 생성 및 배포하고자 합니다.

아래와 같이 git repository에서 소스를 다운로드 합니다. 

```c
$ git clone https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson
```

ggv2-deploy-cloud 디렉토리 아래에 있는 config.json을 편집합니다. 여기서, Account에는 AWS 사용자 ID를 넣고, S3Bucket에 적당한 이름을 부여합니다. 


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
        "S3Bucket": "greengrass",
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

아래와 같이 cloud-_g_command-deploy_cloud에서 create_gg_component.sh을 실행합니다. 

```c
cd aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson/ggv2-deploy-cloud로 이동합니다.

sudo chmod +x create_gg_component.sh

./create_gg_component.sh
```

상기와 같이 shell script를 실행하면 아래와 같은 결과를 얻을 수 있습니ㅏ다. 

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
                "arn": "arn:aws:greengrass:ap-northeast-2:677146750822:components:com.example.ImgClassification:versions:1.0.0"
            }, 
            "arn": "arn:aws:greengrass:ap-northeast-2:677146750822:components:com.example.ImgClassification"
        }, 
        {
            "componentName": "com.example.HelloMqtt", 
            "latestVersion": {
                "publisher": "Amazon", 
                "description": "My first AWS IoT Greengrass component.", 
                "componentVersion": "1.0.0", 
                "platforms": [
                    {
                        "attributes": {
                            "os": "linux"
                        }
                    }
                ], 
                "creationTimestamp": 1655242730.65, 
                "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.HelloMqtt:versions:1.0.0"
            }, 
            "arn": "arn:aws:greengrass:ap-northeast-2:123456789012:components:com.example.HelloMqtt"
        }
    ]
}
```


