## Amazon S3을 이용한 Greengrass device 배포환경 구축하기 

아래의 Policy를 가지는 "GGv2WorkshopS3Policy"을 생성합니다. 

```java
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::*"
    }
  ]
}
```

"GreengrassV2TokenExchangeRole"에 "GGv2WorkshopS3Policy" Policy를 추가합니다.


![noname](https://user-images.githubusercontent.com/52392004/173942768-ee8bbb64-bcbf-4c17-9d34-9056a060d1c8.png)


아래와 같이 S3를 Artifact로 가지는 recipe 파일을 생성합니다. 기존 local deployment와 비교하여 Artifacts에 S3 URI가 추가되었습니다.

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
        "URI": "s3://greengrass-ksdyb/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py"
    }]
  }]
}
```

아래과 같이 이전에 생성한 s3의 "MYBUCKET"에 Recipes, Artifacts 파일들을 복사합니다. 

```c
$ aws s3 cp --recursive ~/GGv2Dev/ s3://$MYBUCKET
upload: ../GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py to s3://greengrass-ksdyb/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py
upload: ../GGv2Dev/recipes/com.example.HelloMqtt-1.0.0.json to s3://greengrass-ksdyb/recipes/com.example.HelloMqtt-1.0.0.json
```

아래의 명령어로 실행합니다. 

```java
$ cd ~/GGv2Dev/recipes && aws greengrassv2 create-component-version  \
--inline-recipe fileb://com.example.HelloMqtt-1.0.0.json \
--region $AWS_DEFAULT_REGION
```

