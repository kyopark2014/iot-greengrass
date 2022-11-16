# Greengrass 명령어와 중요한 메모들

## Greengrass Preparation

- Greengrass installer 다운로드

```java
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

- Greengrass 설치 

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

## Docker Container

- Docker Group User 등록

아래와 같이 Docker 이미지를 구동하기 위하여 ggc_user에 docker를 추가합니다.

```java
sudo usermod -aG docker ggc_user
```

## Inference Image Debugging

Docker 이미지에 설치된 라이브러리 버전등이 학습 환경과 다른 경우에, 정상적으로 동작하지 않을수 있습니다. 이를 확인하려면, 인프라를 설치(Deploy)한 후에 로그를 통해 확인하여야 하는데, 반복적으로 인프라를 설치하면서 디버깅하는 과정은 시간을 많이 소모합니다. 아래에서는 docker 이미지에서 직접 테스트하는 방법을 보여주고 있습니다. 

Docker 소스로 이동하여 이미지를 빌드합니다. 

```java
cd src
docker build -t inference:v1 .
```

빌드된 이미지를 확인합니다. 

```java
docker images
```

Docker를 실행합니다. 
```java
docker run -d -p 8080:8080 inference:v1
```


Docker의 실행된 container 정보를 확인합니다. 

```java
docker ps
```

아래와 같이 Container ID를 확인 할 수 있습니다. 

```java
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
41e297948511   inference:v1   "/lambda-entrypoint.…"   6 seconds ago   Up 4 seconds   0.0.0.0:8080->8080/tcp   stupefied_carson
```

아래와 같이 Bash shell로 접속합니다. 

```java
docker exec -it  41e297948511 /bin/bash
```

[inference-test.py](https://github.com/kyopark2014/lambda-with-ML-container/blob/main/src/inference-test.py)는 [samples.json](https://github.com/kyopark2014/lambda-with-ML-container/blob/main/src/samples.json)을 로드하여 Lambda의 event와 동일한 input을 만든 후에, [inference.py](https://github.com/kyopark2014/lambda-with-ML-container/blob/main/src/inference.py)을 테스트합니다. 따라서, "python3 inference-test.py"와 같이 실행하여, inference.py가 정상적으로 동작하는지 확인할 수 있습니다.

```java
bash-4.2# python3 inference-test.py
np version:  1.23.4
pandas version:  1.5.1
xgb version:  1.6.2
event:  {'body': '[{"fixed acidity":6.6,"volatile acidity":0.24,"citric acid":0.28,"residual sugar":1.8,"chlorides":0.028,"free sulfur dioxide":39,"total sulfur dioxide":132,"density":0.99182,"pH":3.34,"sulphates":0.46,"alcohol":11.4,"color_red":0,"color_white":1},{"fixed acidity":8.7,"volatile acidity":0.78,"citric acid":0.51,"residual sugar":1.7,"chlorides":0.415,"free sulfur dioxide":12,"total sulfur dioxide":66,"density":0.99623,"pH":3.0,"sulphates":1.17,"alcohol":9.2,"color_red":1,"color_white":0}]', 'isBase64Encoded': False}
event:  {'body': '[{"fixed acidity":6.6,"volatile acidity":0.24,"citric acid":0.28,"residual sugar":1.8,"chlorides":0.028,"free sulfur dioxide":39,"total sulfur dioxide":132,"density":0.99182,"pH":3.34,"sulphates":0.46,"alcohol":11.4,"color_red":0,"color_white":1},{"fixed acidity":8.7,"volatile acidity":0.78,"citric acid":0.51,"residual sugar":1.7,"chlorides":0.415,"free sulfur dioxide":12,"total sulfur dioxide":66,"density":0.99623,"pH":3.0,"sulphates":1.17,"alcohol":9.2,"color_red":1,"color_white":0}]', 'isBase64Encoded': False}
isBase64Encoded:  False
Base64 decoding is not required
body:  [{"fixed acidity":6.6,"volatile acidity":0.24,"citric acid":0.28,"residual sugar":1.8,"chlorides":0.028,"free sulfur dioxide":39,"total sulfur dioxide":132,"density":0.99182,"pH":3.34,"sulphates":0.46,"alcohol":11.4,"color_red":0,"color_white":1},{"fixed acidity":8.7,"volatile acidity":0.78,"citric acid":0.51,"residual sugar":1.7,"chlorides":0.415,"free sulfur dioxide":12,"total sulfur dioxide":66,"density":0.99623,"pH":3.0,"sulphates":1.17,"alcohol":9.2,"color_red":1,"color_white":0}]
values:     fixed acidity  volatile acidity  citric acid  residual sugar  ...  sulphates  alcohol  color_red  color_white
0            6.6              0.24         0.28             1.8  ...       0.46     11.4          0            1
1            8.7              0.78         0.51             1.7  ...       1.17      9.2          1            0

[2 rows x 13 columns]
result: [6.573914 4.869721]
200
[6.573914051055908, 4.869720935821533]
Elapsed time: 0.02s
```



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

