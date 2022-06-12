# Greengreen Component

## Greengrass Component 생성

```c
$ mkdir -p ~/GGv2Dev/recipes
$ touch ~/GGv2Dev/recipes/com.example.HelloMqtt-1.0.0.json
```


아래 내용을 receipe에 입력합니다.

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


## Artifact 생성

아래와 같이 "hello_mqtt.py"을 생성합니다. 

```c
mkdir -p ~/GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0
touch ~/GGv2Dev/artifacts/com.example.HelloMqtt/1.0.0/hello_mqtt.py
```

"hello_mqtt.py"에 아래 내용을 입력합니다. 

```python
import json
import time
import os
import random

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()

    while True:
        telemetry_data = {
            "timestamp": int(round(time.time() * 1000)),
            "battery_level": random.randrange(98, 101),
            "location": {
                "longitude": round(random.uniform(101.0, 120.0),2),
                "latitude": round(random.uniform(30.0, 40.0),2),
            },
        }

        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name="ggv2/{}/telemetry".format(os.getenv("AWS_IOT_THING_NAME")),
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=1.0)
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(5)
```

다음 명령어로 로컬 배포를 생성합니다. 

```c
sudo /greengrass/v2/bin/greengrass-cli deployment create \
  --recipeDir ~/GGv2Dev/recipes \
  --artifactDir ~/GGv2Dev/artifacts \
  --merge "com.example.HelloMqtt=1.0.0"
Jun 12, 2022 5:02:01 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onConnectionSetup
INFO: Socket connection /greengrass/v2/ipc.socket:8033 to server result [AWS_ERROR_SUCCESS]
Jun 12, 2022 5:02:01 PM software.amazon.awssdk.eventstreamrpc.EventStreamRPCConnection$1 onProtocolMessage
INFO: Connection established with event stream RPC server
Local deployment submitted! Deployment Id: f414af45-a4d1-4554-8ca3-555c105e89db
```


```c
$ sudo tail -f /greengrass/v2/logs/greengrass.log
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)

2022-06-12T17:02:13.912Z [INFO] (pool-2-thread-93) com.aws.greengrass.deployment.DeploymentService: deployment-task-execution. Finished deployment task. {deploymentId=f414af45-a4d1-4554-8ca3-555c105e89db, serviceName=DeploymentService, currentState=RUNNING}
2022-06-12T17:02:23.952Z [INFO] (pool-2-thread-12) com.aws.greengrass.deployment.DeploymentService: Current deployment finished. {DeploymentId=f414af45-a4d1-4554-8ca3-555c105e89db, serviceName=DeploymentService, currentState=RUNNING}
2022-06-12T17:02:24.002Z [INFO] (pool-2-thread-12) com.aws.greengrass.deployment.DeploymentStatusKeeper: Stored deployment status. {DeploymentId=f414af45-a4d1-4554-8ca3-555c105e89db, DeploymentStatus=FAILED}
2022-06-12T17:02:24.018Z [INFO] (pool-2-thread-12) com.aws.greengrass.deployment.DeploymentDirectoryManager: Persist link to last deployment. {link=/greengrass/v2/deployments/previous-failure}
2022-06-12T17:02:24.018Z [INFO] (pool-2-thread-12) com.aws.greengrass.deployment.DeploymentDirectoryManager: Clean up link to earlier deployment. {link=/greengrass/v2/deployments/previous-success}
2022-06-12T17:04:40.891Z [INFO] (Thread-3) com.aws.greengrass.mqttclient.AwsIotMqttClient: Connection resumed. {clientId=GreengrassCore, sessionPresent=true}
2022-06-12T17:04:40.894Z [INFO] (Thread-3) com.aws.greengrass.status.FleetStatusService: fss-status-update-published. Status update published to FSS. {serviceName=FleetStatusService, currentState=RUNNING}
2022-06-12T17:04:40.895Z [WARN] (Thread-3) com.aws.greengrass.mqttclient.AwsIotMqttClient: Connection interrupted. {clientId=GreengrassCore, error=The connection was closed unexpectedly.}
2022-06-12T17:04:48.095Z [INFO] (Thread-3) com.aws.greengrass.mqttclient.AwsIotMqttClient: Connection resumed. {clientId=GreengrassCore, sessionPresent=true}
2022-06-12T17:04:48.115Z [WARN] (Thread-3) com.aws.greengrass.mqttclient.AwsIotMqttClient: Connection interrupted. {clientId=GreengrassCore, error=The connection was closed unexpectedly.}
2022-06-12T17:04:48.319Z [INFO] (Thread-3) com.aws.greengrass.mqttclient.AwsIotMqttClient: Connection resumed. {clientId=GreengrassCore, sessionPresent=true}
2022-06-12T17:04:48.333Z [INFO] (Thread-3) com.aws.greengrass.deployment.IotJobsHelper: No deployment job found. {ThingName=GreengrassCore}
2022-06-12T17:04:48.334Z [INFO] (Thread-3) com.aws.greengrass.deployment.IotJobsHelper: No deployment job found. {ThingName=GreengrassCore}
2022-06-12T17:04:48.335Z [INFO] (Thread-3) com.aws.greengrass.deployment.IotJobsHelper: No deployment job found. {ThingName=GreengrassCore}
```

## 결과 확인 

1) MQTT test clinet로 이동합니다. 

https://ap-northeast-2.console.aws.amazon.com/iot/home?region=ap-northeast-2#/test


로컬 Greengrass 컴포넌트를 테스트한 후 다음 명령어로 Core 디바이스를 제거합니다.

```c
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove="com.example.HelloMqtt"
```

## 참고
로컬 Greengrass 컴포넌트를 재 시작하려면 다음 명령어를 사용합니다.

```c
sudo /greengrass/v2/bin/greengrass-cli component restart --names "com.example.HelloWorld"
```

설치된 Greengrass 컴포넌트를 확인하려면 다음 명령어를 사용합니다.

```c
sudo /greengrass/v2/bin/greengrass-cli component list
```
