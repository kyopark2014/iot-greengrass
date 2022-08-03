# Greengrass Component

## Component의 특징

- 하나의 Component는 Recipe file과 Artifacts로 구성됩니다. 

- Component의 dependency를 yaml 파일 안에 ComponentDependencies에 정의 할 수 있습니다. 

- Component는 ComponentName과 ComponentVersion으로 구분합니다.

- Component states: RUNNING, FINISHED, ERRORED, BROKEN

- AWS에서 제공하는 Components: Nucleus, Greengrass CLI, Log manager, Stream manager, Local debug console, Secret manager, Secure tunneling 등이 있습니다. 

<img width="929" alt="image" src="https://user-images.githubusercontent.com/52392004/181392075-43f385db-222d-4506-9727-5f0aa7211619.png">


## Artifacts

component를 통해서 실행될 코드 부분인 Artifacts에는 스크립트, 컴파일된 코드, 정적 리소스등이 포함합니다. Component는 종속적으로 지정된 구성요소의 다른 artifacts도 사용할 수 있습니다. 

### Artifacts 예제

## Receipe 예제

```java
---
RecipeFormatVersion: 2020-01-25
ComponentName: demo.example.hello_world
ComponentVersion: '1.0.0'
ComponentDescription: My first AWS IoT Greengrass component.
ComponentPublisher: Amazon
ComponentDependencies:
  aws.greengrass.TokenExchangeService:
    VersionRequirement: '>=0.0.0'
    DependencyType: HARD
ComponentConfiguration:
  DefaultConfiguration:
    Message: world
Manifests:
  - Platform:
      os: linux
    Lifecycle:
      Run: |
        while true; do
          python3 {artifacts:path}/hello_world.py \
            '{configuration:/Message}’
          sleep 5
        done
     Artifacts:
       - URI: s3://BUCKET/artifacts/demo.example.hello_world/…
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


## Reference 

[AWS re:Invent 2020: Dive deep and accelerate your implementation of AWS IoT Greengrass 2.0](https://www.youtube.com/watch?v=t2x49uZuTwE)
