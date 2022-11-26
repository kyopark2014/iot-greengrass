# Greengrass 명령어와 중요한 메모들

## Greengrass Preparation

- Greengrass installer 다운로드

아래와 같이 Greengrass를 다운로드합니다.

```java
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

- Greengrass 설치 

아래와 같이 Greengrass 디바이스를 IoT Core Device로 등록할 수 있습니다. 여기서 디바이스 이름은 "GreengrassCore-18163f7ac3e"으로 하였습니다. 여러개의 디바이스를 사용시에는 다른 이름을 사용하여야 합니다. 

```java
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
	--aws-region ap-northeast-2 \
	--thing-name GreengrassCore-18163f7ac3e \
	--thing-group-name GreengrassGroup \
	--component-default-user ggc_user:ggc_group \
	--provision true \
	--setup-system-service true \
	--deploy-dev-tools true
```

Cloud9으로 개발환경을 구성시에는 [Cloud9을 Greengrass 디바이스로 사용하기](https://github.com/kyopark2014/iot-greengrass/blob/main/cloud9.md)을 참조합니다. 

## Docker Container

[Docker Container 준비](https://github.com/kyopark2014/iot-greengrass/blob/main/docker-component.md#docker-container-preparation)에 따라 greengrass를 docker user group에 등록하고, ECR 퍼미션을 부여합니다. 

## Commands

- Greengrass-cli 버전 확인 

```java
/greengrass/v2/bin/greengrass-cli -V
Greengrass CLI Version: 2.5.6
```

- Component 리스트 확인하기 

```java
sudo /greengrass/v2/bin/greengrass-cli component list
```

- 배포를 위한 Bucket에 파일 복사

```java
MYBUCKET=greengrass-bucketname
aws s3 cp --recursive ~/GGv2Dev/ s3://$MYBUCKET
```

- Local 배포전 Greengrass 서버에 component 등록 

```java
aws greengrassv2 create-component-version  \
--inline-recipe fileb://com.example.HelloMqtt-1.0.0.json \
--region $AWS_DEFAULT_REGION
```

- S3를 이용한 배포전에 Greengrass에 component 등록 

```java
sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ~/GGv2Dev/recipes \
  --artifactDir ~/GGv2Dev/artifacts \
  --merge "com.example.HelloMqtt=1.0.0"
```

- Greengree 로그 확인 

```java
sudo tail -f /greengrass/v2/logs/greengrass.log
```

- Component 로그 확인 

```java
sudo tail -f /greengrass/v2/logs/com.example.HelloMqtt.log
```

- Component 재시작 

```java
sudo /greengrass/v2/bin/greengrass-cli component restart --names "com.example.HelloWorld"
```

- Component 삭제 

```java
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.example.HelloMqtt"
```


- Greengrass 재시작

```java
sudo systemctl restart greengrass.service
```

## 중요한 메모

- Receipe 예제 

```java
{
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "com.example.HelloMqtt",
    "ComponentVersion": "1.0.0",
    "ComponentDescription": "My first AWS IoT Greengrass component.",
    "ComponentPublisher": "Amazon",
    "ComponentConfiguration": {
        "DefaultConfiguration": {
            "accessControl": {
                "aws.greengrass.ipc.mqttproxy": {
                    "com.example.HelloMqtt:mqttproxy:1": {
                        "policyDescription": "Allows access to publish to all AWS IoT Core topics.",
	                    "operations": [
	                        "aws.greengrass#PublishToIoTCore"
	                    ],
	                    "resources": [
	                        "*"
	                    ]
	                }
                }
            }
        }
    },
    "Manifests": [{
        "Platform": {
            "os": "linux"
        },
        "Lifecycle": {
            "Install": {
                "RequiresPrivilege": true,
                "Script": "pip3 install awsiotsdk"
            },
            "Run": "python3 {artifacts:path}/hello_mqtt.py"
        },
        "Artifacts": [{
            "URI": "s3://greengrass-bucketname/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py"
        }]
    }]
}
```



```java
{
    "RecipeFormatVersion": "2020-01-25",
    "ComponentName": "com.example.HelloMqtt",
    "ComponentVersion": "1.0.0",
    "ComponentDescription": "My first AWS IoT Greengrass component.",
    "ComponentPublisher": "Amazon",
    "ComponentConfiguration": {
        "DefaultConfiguration": {
	        "accessControl": {
                "aws.greengrass.ipc.mqttproxy": {
                    "com.example.HelloMqtt:mqttproxy:1": {
                        "policyDescription": "Allows access to publish to all AWS IoT Core topics.",
                        "operations": [
                            "aws.greengrass#PublishToIoTCore"
                        ],
                        "resources": [
                            "*"
                        ]
                    }
                }
            }
        }
    },
    "Manifests": [{
        "Platform": {
            "os": "linux"
        },
        "Lifecycle": {
            "Install": {
                "RequiresPrivilege": true,
                "Script": "sudo pip3 install awsiotsdk"
            },
            "Run": "python3 {artifacts:path}/hello_mqtt.py"
        }
    }]
}
```

## Cloud9에서 EBS 크기 변경

[Cloud9에서 EBS 크기 변경](https://github.com/kyopark2014/technical-summary/blob/main/resize.md)에 따라 cloud9의 볼륨을 조정할 수 있습니다.

## Basic Docker Commends

- Docker 소스로 이미지를 빌드합니다. 

```java
docker build -t example:v1 .
```

- 빌드된 이미지를 확인합니다. 

```java
docker images
```

- Docker를 실행합니다. 

```java
docker run -d -p 8080:8080 example:v1
```


- Docker의 실행된 container 정보를 확인합니다. 

```java
docker ps

CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
41e297948511   example:v1   "/lambda-entrypoint.…"   6 seconds ago   Up 4 seconds   0.0.0.0:8080->8080/tcp   stupefied_carson
```

- Bash shell로 접속합니다.

```java
docker exec -it  41e297948511 /bin/bash
```



