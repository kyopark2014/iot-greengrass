# Greengrass 명령어와 중요한 메모들

- Greengrass installer 다운로드

```c
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassCore
```

- Greengrass 설치 

```c
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
--aws-region ap-northeast-2 \
--thing-name GreengrassQuickStartCore-1815d42ba73 \
--thing-group-name GreengrassQuickStartGroup \
--component-default-user ggc_user:ggc_group \
--provision true \
--setup-system-service true \
--deploy-dev-tools true
```

- Greengrass-cli 버전 확인 

```c
$ /greengrass/v2/bin/greengrass-cli -V
Greengrass CLI Version: 2.5.6
```

- Component 리스트 확인하기 

```c
$ sudo /greengrass/v2/bin/greengrass-cli component list
```

- 배포를 위한 Bucket에 파일 복사

```c
MYBUCKET=greengrass-bucketname
aws s3 cp --recursive ~/GGv2Dev/ s3://$MYBUCKET
```

- Local 배포전 Greengrass 서버에 component 등록 

```c
$ aws greengrassv2 create-component-version  \
--inline-recipe fileb://com.example.HelloMqtt-1.0.0.json \
--region $AWS_DEFAULT_REGION
```

- S3를 이용한 배포전에 Greengrass에 component 등록 

```c
$ sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ~/GGv2Dev/recipes \
  --artifactDir ~/GGv2Dev/artifacts \
  --merge "com.example.HelloMqtt=1.0.0"
```

- Greengree 로그 확인 

```c
$ sudo tail -f /greengrass/v2/logs/greengrass.log
```

- Component 로그 확인 

```c
$ sudo tail -f /greengrass/v2/logs/com.example.HelloMqtt.log
```

- Component 재시작 

```c
$ sudo /greengrass/v2/bin/greengrass-cli component restart --names "com.example.HelloWorld"
```

- Component 삭제 

```c
$ sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.example.HelloMqtt"
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

- Artifact 예제 

```python

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

