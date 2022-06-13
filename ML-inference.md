# 디바이스에서의 ML Inference


## Component 생성

[ML Greengrass 컴포넌트 생성](https://catalog.us-east-1.prod.workshops.aws/workshops/0b21ceb7-2108-4a82-9e76-4c56d4b52db5/ko-KR/5/1)에 좀 더 자세한 내용이 있습니다.

git을 EC2에 설치합니다.

```c
$ sudo yum install git -y
```


소스코드를 다운로드 합니다.

```c
$ git clone https://github.com/aws-samples/aiot-e2e-sagemaker-greengrass-v2-nvidia-jetson
```

ggv2-deploy-cloud 디렉토리 아래에 있는 config.json을 편집합니다.
"Account"를 앞에서 확인한 12자리 계정 번호로 변경한 후 "[YOUR-S3-BUCKET]"을 아래 그림처럼 ***mybucket-[My Account Number]***형식의 버킷 이름으로 교체합니다.
아래 그림은 계정 번호가 123451234123인 경우에 대한 예 입니다.


```java
{
    "Project": {
        "Name": "MLInferenceFromScratch",
        "Account": "1234512345123",
        "Region": "us-east-1",
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
        "S3Bucket": "[YOUR-S3-BUCKET]",
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

AWS Account ID는 아래처럼 확인 할 수 있습니다. 

```c
$ aws sts get-caller-identity --query Account --output text
```

