# Inter-process Communication

## Component 들의 통신방법

각 Component들은 Authorization policies에 따른 권한을 가지고 있습니다. Local componet들 사이와 Local Compent 또는 IoTMQTTClient 사이는 PUBSUB을 사용합니다. 여기서 IoTMQTTClient는 IoT Core와 MQTT 통신을 합니다. 

Recipy의 "accessControl"를 이용하여 Autorization policies를 정의 할 수 있는데, 기본적으로 모든 Component는 nucleus와 IPC 통신을 합니다. 


### IPC service identifier

IPC service identifier는 aws.greengrass.ipc.mqttproxy 입니다. 이를 위해 아래와 같이 policy를 정의 할 수 있습니다. 

[Example authorization policy with limited access](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html)

```java
{
  "accessControl": {
    "aws.greengrass.ipc.mqttproxy": {
      "com.example.MyIoTCorePubSubComponent:mqttproxy:1": {
        "policyDescription": "Allows access to publish/subscribe to factory 1 topics.",
        "operations": [
          "aws.greengrass#PublishToIoTCore",
          "aws.greengrass#SubscribeToIoTCore"
        ],
        "resources": [
          "factory/1/actions",
          "factory/1/events"
        ]
      }
    }
  }
}
```


### 동작 프로세스

1) Component1과 Component2가 Necleus에 IPC로 연결됩니다.

2) Neucleus는 recipe에서 authorization policy를 확인합니다. 여기서 Component1은 topicA에 locally publish가 가능하고, Component2는 topicA를 subscribe하고 topicB를 publish 할 수 있습니다. 

3) Component1이 Component2에 메시지를 보내기 위해서 publish를 하면, PubSub service를 통해 topicA를 subscribe하고 있는 Component2로 메시지를 전달할 수 있습니다. 

4) Component2가 topicB로 Publish를 하면, IoTMqtt service가 이를 받아서 IoT Core로 전송할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/181382025-d2a786dd-b2f1-46a7-9cc5-065ae749c54d.png)

#### Recipy 예제 

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

## Local IPC connection 예

[AWS IoT Greengrass V2 | MQTT Applications ](https://www.youtube.com/watch?v=hAZ-nlAaSvw)와 같이 IPC sdk를 이용하여 IPC 연결 할 수 있습니다. 

![image](https://user-images.githubusercontent.com/52392004/182856688-2c9ffc38-5ceb-4ea7-b919-f95111663f94.png)

```java
---
RecipeFormatVersion: 2020-01-25
ComponentName: com.example.HelloWorld
ComponentVersion: '1.1.0'
ComponentDescription: My first AWS IoT Greengrass component.
ComponentPublisher: Michael
ComponentConfiguration:
  DefaultConfiguration: {}
Manifests:
  - Platform:
      os: '*'
    Lifecycle:
      Run: |
        PYTHONPATH="{artifacts:decompressedPath}/helloWorld/dependencies" python3 -u {artifacts:decompressedPath}/helloWorld/hello_world.py
     Artifacts:
       - URI: s3://BUCKET/artifacts/com.example.HelloWorld.zip
        Unarchive: ZIP
```

## Reference

[AWS IoT Greengrass V2 | MQTT Applications ](https://www.youtube.com/watch?v=hAZ-nlAaSvw)
