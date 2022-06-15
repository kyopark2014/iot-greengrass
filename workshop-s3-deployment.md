## Amazon S3을 이용한 Greengrass device 배포환경 구축하기 

아래의 Policy를 가지는 "GGv2WorkshopS3Policy"을 생성합니다. 

```java
	 {
            "Sid": "DeployDevTools",
            "Effect": "Allow",
            "Action": [
                "greengrass:CreateDeployment",
                "greengrass:GetServiceRoleForAccount",
                "iot:CancelJob",
                "iot:CreateJob",
                "iot:DeleteThingShadow",
                "iot:DescribeJob",
                "iot:DescribeThing",
                "iot:DescribeThingGroup",
                "iot:GetThingShadow",
                "iot:UpdateJob",
                "iot:UpdateThingShadow"
            ],
            "Resource": "*"
        }
```

"GreengrassV2TokenExchangeRole"에 "GGv2WorkshopS3Policy" Policy를 추가합니다.


아래와 같이 S3를 Artifact로 가지는 recipe 파일을 생성합니다.

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

아래과 같이 MYBUCKET에 bucket name을 등록하고, 아래와 같이 python 파일을 복사합니다. 

```c
$ aws s3 cp --recursive ~/GGv2Dev/ s3://$MYBUCKET
upload: ../GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py to s3://greengrass-ksdyb/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py
upload: ../GGv2Dev/recipes/com.example.HelloMqtt-1.0.0.json to s3://greengrass-ksdyb/recipes/com.example.HelloMqtt-1.0.0.json
```


아래의 명령어로 실행합니다. 

```java
$ cd ~/GGv2Dev/recipes && aws greengrassv2 create-component-version  --inline-recipe fileb://com.example.HelloMqtt-1.0.0.json --region $AWS_DEFAULT_REGION
```

